import mediapipe as mp
import numpy as np
import math
import cv2 as cv
import detector_hand_face_module as hcm

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils

# this lines for initialize the volume module 

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

print(volume.GetVolumeRange())
# volume.SetMasterVolumeLevel(-20.0, None)


cap = cv.VideoCapture(0)

detector = hcm.HandTracker(min_detection_confidence = 0.8) 

volBar = 400

while True:
    ret, image = cap.read()
    
    # hand detector
    image = detector.find_hands(image)

    #find the position of each fingre

    position = detector.find_position(image)

    if len(position) != 0:
        # print(position[4], position[8])
        x1, y1 = position[4][1], position[4][2]
        x2, y2 = position[8][1], position[8][2]  
        cv.circle(image, (x1, y1), 8, (255, 0, 255), cv.FILLED)
        cv.circle(image, (x2, y2), 8, (255, 0, 255), cv.FILLED) 

        cv.line(image, (x1, y1), (x2, y2), (255, 0, 255), 2)   

        cx = (x1+x2) // 2
        cy = (y1+y2) // 2

        length = math.sqrt((x1-x2)**2 + (y1-y2)**2)

        if length < 15:
            cv.circle(image, (cx, cy), 8, (0, 255, 100), cv.FILLED) 
        else:
            cv.circle(image, (cx, cy), 8, (255, 0, 255), cv.FILLED) 

        # print(length)

        #converting the length values into volume range values 

        vol = np.interp(length, [11, 200], [-96, 0])
        volBar = np.interp(length, [11, 200], [400, 150])
        volperc = np.interp(length, [11, 200], [0, 100])

        print(vol)

        cv.rectangle(image, (50, 150), (85, 400), (255, 0, 0), 3)
        cv.rectangle(image, (50, int(volBar)), (85, 400), (0, 0, 255), cv.FILLED)
        cv.putText(image, f'{int(volperc)}%', (50, 120), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        
        # controling volume

        volume.SetMasterVolumeLevel(vol, None)


    cv.imshow('my webcam', image)

    key = cv.waitKey(1)

    if key == ord('e'):
        break

cap.release()
cv.destroyAllWindows()