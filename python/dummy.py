import time
import sys

from Adafruit_IO import MQTTClient

User = 'raebelchristo'
Key = 'aio_NHyV71dLrRu5QBLqhs0vT364IHTS'

client = MQTTClient(User, Key)

client.connect()

foo = input('Input slot ID: ')

client.publish('leavingcar', foo)

client.disconnect()