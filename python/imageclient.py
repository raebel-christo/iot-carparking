import picamera
import struct
import socket
import io
import time


def establish_connection(sock):
    c = 1
    while True:
        try:
            sock.connect(('192.168.1.101',8000))
        except socket.error as e:
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

while True:
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
