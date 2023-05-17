import time
from Adafruit_IO import MQTTClient
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

kit.servo[7].set_pulse_width_range(700,2400)
kit.servo[8].set_pulse_width_range(700,2400)

USER = 'raebelchristo'
KEY = 'aio_NHyV71dLrRu5QBLqhs0vT364IHTS'

def connected(client):
    if client.subscribe('leavingcar'):
        print("Connected to feeds: [leavingcar]")

def disconnected(client):
    print('MQTT has disconnected')

def message(client, feed, payload):
    global kit
    print(f'{feed} has sent {payload}')
    if payload == '-2': #open exit
        kit.servo[7].angle = 90
    if payload == '-1': #close all
        kit.servo[7].angle = 170
        kit.servo[8].angle = 10
    if payload == '-3': #open entry
        kit.servo[8].angle = 90


client = MQTTClient(USER,KEY)

client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.connect()

while True:
    client.loop_background()