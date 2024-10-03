import numpy as np
import cv2

import mediapipe as mp

cap = cv2.VideoCapture(0)

# intialize hand modul 

mpHands = mp.solutions.hands
hands = mpHands.Hands()

npdrow = mp.solutions.drawing_utils # this line is for drowing the point of every single hand

while True :
    ret, frame = cap.read

    imrgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(imrgb)

    # print(result.multi_hand_landmarks)

    if result.multi_hand_landmarks :
        for hand in result.multi_hand_landmarks :
            for id, lm in enumerate(hand.landmark):
                # print(id, lm)
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h) 
                print(id, cx, cy)
                if id < 10 :
                    cv2.circle(frame, (cx, cy), 10, (100, 255, 29), cv2.FILLED)

            npdrow.draw_landmarks(frame, hand, mpHands.HAND_CONNECTIONS)


    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('e'):
        break

cap.release()
cv2.destroyAllWindows()