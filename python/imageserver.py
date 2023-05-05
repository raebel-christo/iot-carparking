import io
import socket
import struct
from PIL import Image
import matplotlib.pyplot as plotter
import keyboard
import pytesseract
import cv2 as cv
import numpy as np
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def scanText(image):
    extractedText = ""
    cvimage = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
    grayimage = cv.cvtColor(cvimage, cv.COLOR_BGR2GRAY)
    thres = cv.threshold(grayimage,0,255,cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
    opening = cv.morphologyEx(grayimage,cv.MORPH_OPEN, np.ones((5,5),np.uint8))
    canny = cv.Canny(grayimage, 100,200)

    for img in [cvimage, grayimage, thres, opening, canny]:
        d = pytesseract.image_to_data(img, output_type=Output.DICT)
        n_boxes = len(d['text'])

        if len(img.shape) == 2:
            img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
        
        for i in range(n_boxes):
            if int(d['conf'][i]) > 60:
                (text, x, y, w, h) = (d['text'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                if text and text.strip() != "":
                    img = cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    img = cv.putText(img, text, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                    extractedText = extractedText + text.strip()
        
                print("Confidence Level: {0} > \"{1}\"".format(d['conf'][i], d['text'][i]))
            elif int(d['conf'][i]) > 20:
                (text, x, y, w, h) = (d['text'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                if text and text.strip() != "":
                    img = cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    img = cv.putText(img, text, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 1)
                print("Confidence Level: {0} > \"{1}\"".format(d['conf'][i], d['text'][i]))
        
        print("Scan Complete")
        cv.imshow('img', img)
        if(extractedText != ""):
            print("Number plate is " + extractedText)
            cv.waitKey(0)



websocket = socket.socket()
websocket.bind(('192.168.1.101',8000))
websocket.listen(0)

connection = websocket.accept()[0].makefile('rb')

try:
    img = None
    while True:
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
        scanText(image)
except:
    print("Terminating")
    connection.close()
    websocket.close()
    exit(1)

finally:
    connection.close()
    websocket.close()
