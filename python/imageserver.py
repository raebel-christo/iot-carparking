#Socket libraries
import io
import socket
import struct
from PIL import Image

#Image Processing libraries
import matplotlib.pyplot as plotter
import keyboard
import pytesseract
import cv2 as cv
import numpy as np
from pytesseract import Output
import re

#Database libraries
import pymongo
import pytz
import time
import datetime as datetime

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
            cv.waitKey(2)
            break

    return extractedText    

uri = "mongodb+srv://raebelchristo:amber47@cluster0.c50zie8.mongodb.net/?retryWrites=true&w=majority"
database = pymongo.MongoClient(uri)
if database:
    print("Database Connected")
collection = database['carparking']['cars']

websocket = socket.socket()
websocket.bind(('192.168.1.101',8000))
websocket.listen(0)

connection = websocket.accept()[0].makefile('rb')



try:
    img = None
    running = True
    while running:
        image_len = struct.unpack('<L',connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break

        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        image_stream.seek(0)

        image = Image.open(image_stream)
        # plotter.imshow(image)
        
        # plotter.pause(0.01)
        # plotter.close()
        print("Scanning image")
        extractedText = scanText(image)
        current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

        if not emptyText(extractedText):
            for i in range(1,5):
                if not collection.find_one({"slot":"{0}".format(i)}):
                    x = collection.insert_one({
                        "slot":"{0}".format(i),
                        "plate":"{0} {1}".format(extractedText[0], extractedText[1]),
                        "in_time":current_time
                    })
                    print(x)
                    running = False

except Exception as e:
    print("Terminating due to " + e)
    connection.close()
    websocket.close()
    exit(1)

finally:
    connection.close()
    websocket.close()
