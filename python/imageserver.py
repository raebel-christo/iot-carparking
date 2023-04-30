import io
import socket
import struct
from PIL import Image
import matplotlib.pyplot as plotter

websocket = socket.socket()
websocket.bind('192.168.1.101', 8000)