import mediapipe as mp
import cv2 as cv
import numpy as np

mp_holistic = mp.solutions.holistic
holistic_model = mp_holistic.Holistic()

mp_Hands = mp.solutions.hands
hands_model = mp_Hands.Hands()

drow_landmarks = mp.solutions.drawing_utils

cap = cv.VideoCapture(0)


def drow_hand_landmarks(hands_coordonats, frame) :
    if hands_coordonats :
        for hand in hands_coordonats :
            drow_landmarks.draw_landmarks(frame, hand, mp_Hands.HAND_CONNECTIONS)


def drow_face_landmarks(face_coordonats, frame) :
    
    if face_coordonats :
        drow_landmarks.draw_landmarks(
            frame, 
            face_coordonats, 
            mp_holistic.FACEMESH_CONTOURS,
            
            drow_landmarks.DrawingSpec(
                color=(255,0,255),
                thickness=1,
                circle_radius=1
            ),
            drow_landmarks.DrawingSpec(
                color=(0,255,255),
                thickness=1,
                circle_radius=1
            )
        )
            

while True :
    rat, frame = cap.read()
    imageToRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results_hands = hands_model.process(imageToRGB)
    results_faces = holistic_model.process(imageToRGB)

    # print(results_hands.multi_hand_landmarks)
    # print(results_faces.face_landmarks)

    drow_hand_landmarks(results_hands.multi_hand_landmarks, frame)

    # frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

    drow_face_landmarks(results_faces.face_landmarks, frame)

    cv.imshow("frame", frame)

    if cv.waitKey(1) == ord('e'):
        break

cap.release()
cv.destroyAllWindows()