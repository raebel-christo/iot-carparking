import picamera
import struct
import socket
import io
import time

websocket = socket.socket()
websocket.connect(('192.168.1.101', 8000))

connection = websocket.makefile('wb')

try:

    camera = picamera.PiCamera()
    camera.resolution = (500,480)
    camera.vflip = True
    camera.hflip = True
    camera.start_preview()
    time.sleep(2)

    stream = io.BytesIO()

    for foo in camera.capture_continuous(stream, 'jpeg'):
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        stream.seek(0)
        connection.write(stream.read())
        stream.seek(0)
        stream.truncate()
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Terminating Camera Stream")
    connection.write(struct.pack('<L', 0))

finally:
    connection.close()
    websocket.close()
