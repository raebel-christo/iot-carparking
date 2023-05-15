#Socket libraries
import io
import socket
import struct
from PIL import Image

#Image Processing libraries
import matplotlib.pyplot as plotter
import pytesseract
import cv2 as cv
import numpy as np
from pytesseract import Output
import re

#Database libraries
import pymongo
import pytz
import datetime

#Adafruit libraries
from Adafruit_IO import MQTTClient

#Helper libraries
import queue

USER = 'raebelchristo'
KEY = 'aio_NHyV71dLrRu5QBLqhs0vT364IHTS'

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

callback_queue = queue.Queue()

uri = "mongodb+srv://raebelchristo:amber47@cluster0.c50zie8.mongodb.net/?retryWrites=true&w=majority"
database = pymongo.MongoClient(uri)
if database:
    print("Database Connected")

collection = database['carparking']['cars']

websocket = socket.socket()
websocket.bind(('192.168.1.101',8000))
websocket.listen(10)

def mainThreadCall():
    global callback_queue
    while True:
        try:
            callback = callback_queue.get(False)
        except queue.Empty:
            break
        callback()

def emptyText(text):
    if text[0].strip() != "" and text[1].strip() != "":
        return False
    return True

def scanText(image):
    extractedText = ["",""]
    elementFound=False
    cvimage = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
    grayimage = cv.cvtColor(cvimage, cv.COLOR_BGR2GRAY)
    thres = cv.threshold(grayimage,0,255,cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
    opening = cv.morphologyEx(grayimage,cv.MORPH_OPEN, np.ones((5,5),np.uint8))
    canny = cv.Canny(grayimage, 100,200)

    for img in [cvimage, grayimage, thres, opening, canny]:
        if elementFound is True:
            print("Exiting image scanning")
            break
        d = pytesseract.image_to_data(img, output_type=Output.DICT)
        n_boxes = len(d['text'])

        if len(img.shape) == 2:
            img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
        
        for i in range(n_boxes):
            if int(d['conf'][i]) > 70:
                (text, x, y, w, h) = (d['text'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                if text and text.strip() != "":
                    cleanText = text.strip()
                    img = cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    img = cv.putText(img, text, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                    print("Confidence Level: {0} > \"{1}\"".format(d['conf'][i], d['text'][i]))
                    if re.match('[A-Za-z][A-Za-z]\d\d',cleanText) and extractedText[0] == "" and len(cleanText) == 4:
                        extractedText[0] = cleanText
                    if re.match('[A-Z][A-Z]+[0-9]{4}', text.strip()) and extractedText[1] == "" and len(cleanText) == 6:
                        extractedText[1] = cleanText
                    if not emptyText(extractedText):
                        elementFound = True
                        print("Complete Number Plate detected: {0} {1}".format(extractedText[0], extractedText[1]))
                        break
        
        print("Scan Complete")
        if not emptyText(extractedText):
            cv.imshow('img', img)
            cv.waitKey(0)
            cv.destroyAllWindows()
            break

    return extractedText    

def performSocketCommunication(collection, mode, payload=0):
    global websocket
    connection = websocket.accept()[0].makefile('rb')
    try:
        running = True
        while running:
            image_len = struct.unpack('<L',connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break

            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            image_stream.seek(0)

            image = Image.open(image_stream)
            plotter.imshow(image)
            
            plotter.pause(0.01)
            print("Scanning image")

            extractedText = scanText(image)

            current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

            if not emptyText(extractedText):
                if mode == 'insert':
                    for i in range(1,5):
                        if not collection.find_one({"slot":"{0}".format(i)}):
                            x = collection.insert_one({
                                "slot":"{0}".format(i),
                                "plate":"{0} {1}".format(extractedText[0], extractedText[1]),
                                "in_time":current_time
                            })
                            print(x)
                            running = False
                            break
                        elif i==4:
                            print("No space in parking slots")
                            running = False
                elif mode == 'delete':
                    x = collection.delete_one({
                        "slot":f"{payload}"
                    })
                    print(x)
                    running = False
                elif mode == 'query':
                    x = collection.find_one({
                        "plate":"{0} {1}".format(extractedText[0], extractedText[1])
                    }, {
                        "slot":1
                    })
                    if x:
                        print(f"{x['slot']} is leaving")
                        client.publish('leavingcar', int(x['slot']))
                    else:
                        print("Vehicle Not found")
                    running = False            
        plotter.close()

    except Exception as e:
        print(f"Terminating due to [{str(e)}]")
        websocket.close()
        exit(1)

def connected(client):
    print("MQTT Client Connected to Adafruit")
    if client.subscribe('gate-sensor'):
        print("Connected to feeds: [enteringcar]")

def disconnected(client):
    print('MQTT has disconnected')

def message(client, feed, payload):
    global collection
    global callback_queue
    print(f'{feed} has a new value: {payload}')
    if payload == '1':
        print("Vehicle at entry: Performing Insert Operation")
        callback_queue.put(performSocketCommunication(collection,mode='insert'))
        print("Sending 0 to feed")
        client.publish('enteringcar', 0)
    if payload == '2':
        print("Vehicle at entry: Query Operation")
        callback_queue.put(performSocketCommunication(collection,mode='query'))
        print("Sending 0 to feed")
        client.publish('enteringcar', 0)

client = MQTTClient(USER,KEY)

client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.connect()

while True:
    print(".....")
    client.loop_blocking()
    mainThreadCall()