import mediapipe as mp
import cv2 
import detector_hand_face_module as hdm  

detector = hdm.HandTracker(min_detection_confidence = .4)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

colorR = ((255, 0, 255))
x, y, w, h = 100, 100, 200, 200

while True:
    ret, frame = cap.read()  # Read the frame from the webcam
    if not ret:
        break

    frame = detector.find_hands(frame)
    position, _ = detector.find_position(frame)
    l, _, _ = detector.findDistance(frame, 8, 12)

    if l<30:
        if len(position) != 0:
            cursor = position[8]
            if x-w < cursor[1] < x+w and y-h < cursor[2] < y+h:
                colorR = (0, 255, 0)
                id1, x, y = cursor
            else:
                colorR = (255, 0, 255)

    cv2.rectangle(frame, (x-w, y-h), (x+w, y+h), colorR, cv2.FILLED)


    cv2.imshow('Webcam', frame)

    if cv2.waitKey(1) == ord('e'):
        break

cap.release()
cv2.destroyAllWindows()