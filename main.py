import time

import cv2
import numpy as np
import serial
import picamera
import picamera.array

from Image import Image
from Utils import SlicePart, RepackImages

WIDTH = 320
HEIGHT = 240
TOLERANCE = 145
TURN_MAX = 190
TURN_MID = 90

direction = 0

def in_tolerance(n):
    return -TOLERANCE <= n <= TOLERANCE


def calculate_master_point(y_values):
    num_valid = len(y_values)
    weight_factors = [0.7, 0.85, 1, 1.1, 1.2, 1.35]
    master_point = 0

    for i in range(len(y_values)):
        if in_tolerance(y_values[i]):
            master_point += y_values[i] * weight_factors[i]
        else:
            y_values[i] = 0
            num_valid -= 1

    master_point = 2.65 * master_point / (num_valid + 0.1)

    adjustment_factors = [0.5, 0.4, 0.3, -0.4, -0.5, -0.6]
    for i in range(len(y_values)):
        master_point += y_values[i] * adjustment_factors[i]

    return master_point, num_valid

def determine_direction(master_point, num_valid):
    if num_valid < 2:
        return 'B'
    elif master_point > TURN_MID and master_point < TURN_MAX:
        return 'l'
    elif master_point < -TURN_MID and master_point > -TURN_MAX:
        return 'r'
    elif master_point >= TURN_MAX:
        return 'L'
    elif master_point <= -TURN_MAX:
        return 'R'
    else:
        return 'G'

def cmd_cal(la, lb, lc, ld, le, lf):
    l_val = [la, lb, lc, ld, le, lf]
    for i in range(len(l_val)):
        l_val[i] -= WIDTH/2

    master_point, num_valid = calculate_master_point(l_val)
    direction = determine_direction(master_point, num_valid)
    
    cmd = ("%c\n" % (direction)).encode('ascii')

    print(">>> master_point:%d, cmd:%s" % (master_point, cmd))
    
    ser.write(cmd)
    print("send allright")
    time.sleep(0.7)

ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(1)


Images=[]
N_SLICES = 6

for _ in range(N_SLICES):
    Images.append(Image())

camera = picamera.PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30
camera.brightness = 70
camera.contrast = 70
camera.exposure_mode = 'fireworks'

zf = 0.2
camera.zoom = (0+zf, 0+zf, 1-2*zf, 1-2*zf)
rawCapture = picamera.array.PiRGBArray(camera, size = (320, 240))
time.sleep(0.1)


for frame in camera.capture_continuous (rawCapture, format = "bgr", use_video_port = True):

    image = frame.array
    image = cv2.resize(image,(320,240))

    Points = SlicePart(image, Images, N_SLICES)
    fm = RepackImages(Images)

    cmd_cal(Points[0][0], Points[1][0], Points[2][0], Points[3][0], Points[4][0], Points[5][0])

    cv2.imshow('frame', fm)
    rawCapture.truncate(0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      print("Stopped!")
      break

cv2.destroyAllWindows()
