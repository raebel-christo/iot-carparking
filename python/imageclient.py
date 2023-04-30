import picamera
import struct
import time
import socket
import io

websocket = socket.socket()
websocket.connect(('192.168.1.101', 8000))

connection = websocket.makefile('wb')

try:

    camera = picamera.PiCamera()
    camera.resolution = (500,480)
    camera.start_preview()
    time.sleep(2)

    start = time.time()
    stream = io.BytesIO()

    for foo in camera.capture_continuous(stream, 'jpeg'):
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        stream.seek(0)
        connection.write(stream.read())
        stream.seek(0)
        stream.truncate()

except KeyboardInterrupt:
    print("Terminating Camera Stream")
    connection.write(struct.pack('<L', 0))

finally:
    connection.close()
    websocket.close()