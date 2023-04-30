import io
import socket
import struct
from PIL import Image
import matplotlib.pyplot as plotter

websocket = socket.socket()
websocket.bind('192.168.1.101', 8000)

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

        if img is None:
            img = plotter.imshow(image)
        else:
            img.set_data(image)
        
        plotter.pause(0.01)
        plotter.draw()

        image.verify()

finally:
    connection.close()
    websocket.close()