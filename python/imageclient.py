import picamera
import struct
import socket
import io
import time
from Adafruit_IO import MQTTClient

client = MQTTClient('raebelchristo', 'aio_NHyV71dLrRu5QBLqhs0vT364IHTS')

newDataReceived = False

def connected(client):
    client.subscribe('enteringcar')

def disconnected(client):
    print("Lost connection to Adafruit")
    try:
        client.connect()
    except Exception as e:
        print(f"Error occured during reconnection: [{e.strerr}]")
        exit()

def message(client, feed_id, payload):
    print(f"Adafruit sent: [{payload}]")
    if payload==1:
        newDataReceived=True
    else:
        newDataReceived=False

def establish_connection(sock):
    c = 1
    while True:
        try:
            sock.connect(('192.168.1.101',8000))
        except socket.error as e:
            if(e.errno == 106):
                break
            print(f"Retrying connection {c} [{e.strerror}]")
            c = c+1
            time.sleep(2)
        else:
            break
    print("Connected to host")
    connection = sock.makefile('wb')
    print("Initiated stream connection")
    return (connection)

sock = socket.socket()
connection = establish_connection(sock)
client.connect()
client.loop_background()

while True:
    if(newDataReceived):
        try:
            camera = picamera.PiCamera()
            camera.resolution = (900,900)
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
                print("Streamed an image")
                time.sleep(0.5)

        except KeyboardInterrupt:
            print("Terminating Camera Stream")
            connection.write(struct.pack('<L', 0))
            break

        except socket.error as e:
            print(f"Lost connection with host [{e.strerror}]. Retrying connection in 2 seconds")
            time.sleep(2)
            connection = establish_connection(sock)

connection.close()
sock.close()

print("The program has concluded")
