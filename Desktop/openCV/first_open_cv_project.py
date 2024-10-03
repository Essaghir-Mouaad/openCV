import numpy as np
import cv2

import mediapipe as mp

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces :
        # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 133, 0), 1)
        center_x = x + w // 2
        center_y = y + h // 2

        # Determine the radius for the circle (half the width or height of the rectangle, whichever is smaller)
        radius = min(w, h) // 2

        cv2.circle(frame, (center_x, center_y), radius, (144, 0, 0), 2)
        eyse = eye_cascade.detectMultiScale(gray, 1.3, 5)
        for (ex, ey, ew, eh) in eyse :
            cv2.rectangle(frame, (ex, ey), (ex+ew, ey+eh), (0, 50, 0), 2)

    cv2.imshow('😊😊😊😊😊', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
# print(faces)