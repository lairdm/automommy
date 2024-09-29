#!/usr/bin/env python

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to MQTT broker")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic : " + str(mid) +" with QoS" + str(granted_qos))


if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    client.connect("192.168.1.10", 1883, 60)

    client.subscribe("/home/office/monitors", qos=1)

    client.on_connect = on_connect

    client.on_message = on_message

    client.loop_forever()
