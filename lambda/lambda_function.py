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
    
    showstable = dynamo_client.Table(os.environ['DYNAMODB_TABLE'])
    
    intent_name = event['request']['intent']['name']
    
    if intent_name == "dialGate":
        post_message(sqs_client, 'dialGate', queue_url)
        message = "seventh chevron locked. Wormhole active."
    elif intent_name == "playOnTv":
        post_message(sqs_client, 'playOnTv', queue_url)
        showname = event['request']['intent']['slots']['showName']['value'].lower()
        table_row = showstable.get_item(
            Key={
                'showname': showname
            })
        logger.info("show name " + showname)
        logger.info("show slug:")
        logger.info(table_row)
        if "Item" in table_row:
            logger.info(table_row['Item']['slug'])
            sns_client.publish(
                TargetArn=os.environ['SNS_TOPIC'],
                Message=json.dumps({'action': 'play', 'show': table_row['Item']['slug']}))
            message = "Make it so"
        else:
            logger.info("Unknown show")
            message = "Sorry, unknown show or movie"
    else:
        message = "Unknown"
        
    speechlet = build_speechlet_response("Player Status", message, "", "true")
    return build_response({}, speechlet)
