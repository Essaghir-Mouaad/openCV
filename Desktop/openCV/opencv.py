import mediapipe as mp
import numpy as np
import math
import cv2 as cv
import detector_hand_face_module as hcm

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils


cap = cv.VideoCapture(0)

detector = hcm.HandTracker(min_detection_confidence = 0.8) 

volBar = 400

while True:
    ret, image = cap.read()
    
    # hand detector
    image = detector.find_hands(image)

    #find the position of each fingre

    position, _ = detector.find_position(image)

    cv.imshow('my webcam', image)

    key = cv.waitKey(1)

    if key == ord('e'):
        break

cap.release()
cv.destroyAllWindows()