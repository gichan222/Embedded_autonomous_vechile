import time

import cv2
import numpy as np
import serial
import picamera
import picamera.array

from Image import *
from Utils import *

WIDTH = 320
HEIGHT = 240
TOLERANCE = 145
TURN_MAX = 190
TURN_MID = 90

### settting camera
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
time.sleep (0.1)

for frame in camera.capture_continuous (rawCapture, format = "bgr", use_video_port = True):
    # time.sleep(0.1)
    image = frame.array
    image = cv2.resize(image,(320,240))

    # 이미지를 조각내서 윤곽선을 표시하게 무게중심 점을 얻는다
    Points = SlicePart(image, Images, N_SLICES)
    #print('Points : ', Points)

    # 조각난 이미지를 한 개로 합친다
    fm = RepackImages(Images)

    #Display the resulting frame
    cv2.imshow('frame', fm)
    rawCapture.truncate(0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      print("Stopped!")
      break

# Closes all the frames
cv2.destroyAllWindows()
