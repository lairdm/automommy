import boto3
import logging
import json
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

access_key = os.environ["ACCESS_KEY"]
access_secret = os.environ["ACCESS_SECRET"]
region ="us-west-2"
queue_url = os.environ["SQS_QUEUE_URL"]
sqs_client = boto3.client('sqs', aws_access_key_id = access_key, aws_secret_access_key = access_secret, region_name = region)
sns_client = boto3.client('sns')
dynamo_client = boto3.resource('dynamodb')

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def post_message(client, message_body, url):
    response = client.send_message(QueueUrl = url, MessageBody= message_body)
    
def lambda_handler(event, context):
    logger.info("Directive:")
    logger.info(json.dumps(event, indent=4, sort_keys=True))
    
    showstable = dynamo_client.Table(os.environ['DYNAMODB_SHOWS_TABLE'])
    locationstable = dynamo_client.Table(os.environ['DYNAMODB_LOCATIONS_TABLE'])
    
    intent_name = event['request']['intent']['name']
    
    if intent_name == "dialGate":
        post_message(sqs_client, 'dialGate', queue_url)
        message = "seventh chevron locked. Wormhole active."
    elif intent_name == "playOnTv" or intent_name == "playInLocation":
        post_message(sqs_client, 'playOnTv', queue_url)
        showname = event['request']['intent']['slots']['showName']['value'].lower()
        playlocation = event['request']['intent']['slots'].get('playLocation', {'value': 'default'})['value'].lower()
        table_row = showstable.get_item(
            Key={
                'showname': showname
            })
        location_row = locationstable.get_item(
            Key={
                'location': playlocation
            })
        logger.info("intent: " + intent_name)
        logger.info("location " + playlocation)
        logger.info("show name " + showname)
        logger.info("show slug:")
        logger.info(table_row)
        
        if "Item" not in location_row:
            logger.error("Unknown location: " + playlocation)
        elif "Item" not in table_row:
            logger.info("Unknown show: " + showname)
            message = "Sorry, unknown show or movie"
        
        else:
            logger.info(table_row['Item']['slug'])
            logger.info(location_row['Item']['slug'])
            sns_client.publish(
                TargetArn=os.environ['SNS_TOPIC'],
                Message=json.dumps({'action': 'play', 'show': table_row['Item']['slug'], 'location': location_row['Item']['slug']}))
            message = "Make it so"
    else:
        message = "Unknown"
        
    speechlet = build_speechlet_response("Player Status", message, "", "true")
    return build_response({}, speechlet)

def sync_handler(event, context):
    logger.info("Request: %s", event)
    response_code = 200

    http_method = event.get('httpMethod')
    query_string = event.get('queryStringParameters')
    headers = event.get('headers')
    body = event.get('body')

    action = {'action': 'sync'}
    
    if body is not None:
        data = json.loads(body)

        if 'torrent_id' in data:
            action['torrent_id'] = data['torrent_id']

    sns_client.publish(
        TargetArn=os.environ['SNS_TOPIC'],
        Message=json.dumps(action))

    response = {
        'statusCode': response_code,
        'body': json.dumps(action)
    }

    logger.info("Response: %s", response)
    return response
