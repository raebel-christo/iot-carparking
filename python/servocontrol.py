import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

kit.servo[7].set_pulse_width_range(1000,2000)

while True:
    kit.servo[7].angle = 160
    time.sleep(2)
    kit.servo[7].angle = 35
    time.sleep(2)
    kit.servo[7].angle = 90
    time.sleep(2)