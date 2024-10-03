import numpy as np
import cv2
import time
import mediapipe as mp
import math

# Initialize the MediaPipe Hands module
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils  # Drawing utilities for hands

class HandTracker:
    def __init__(self, mode=False, max_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        mode = mode
        max_hands = max_hands
        min_detection_confidence = min_detection_confidence
        min_tracking_confidence = min_tracking_confidence

        # Correct initialization of the Hands class with explicit keyword arguments
        self.hands = mpHands.Hands(static_image_mode=mode,
                                   max_num_hands=max_hands,
                                   min_detection_confidence=min_detection_confidence,
                                   min_tracking_confidence=min_tracking_confidence)

        self.result = None
    
    def find_hands(self, frame):
        # Convert the frame to RGB for processing
        im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame to detect hands
        self.result = self.hands.process(im_rgb)

        if self.result.multi_hand_landmarks:
            for hand_landmarks in self.result.multi_hand_landmarks:
                # Draw the landmarks on the frame
                mpDraw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

        return frame
    

    def find_position(self, frame, drow=True):
        self.lmlist = []
        xlist = []
        ylist = []
        bbox = ()

        if self.result and self.result.multi_hand_landmarks:
            myhand = self.result.multi_hand_landmarks[0]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                self.lmlist.append([id, cx, cy])
                
                if drow:
                    cv2.circle(frame, (cx, cy), 5, (255, 200, 1), cv2.FILLED)

                xlist.append(cx)
                ylist.append(cy)

            xmin, xmax = min(xlist), max(xlist)
            ymin, ymax = min(ylist), max(ylist)
            
            bbox = xmin, xmax, ymin, ymax

            cv2.rectangle(frame, (xmin-20, ymin-20), (xmax+20, ymax+20), (255, 255, 255), 3)
        
        return self.lmlist, bbox
    

    def findDistance(self, frame, p1, p2):
        x1, y1 = 0, 0
        x2, y2 = 0, 0
        length = 0
        cx, cy = 0, 0

        if len(self.lmlist) != 0:
            x1, y1 = self.lmlist[p1][1], self.lmlist[p1][2]
            x2, y2 = self.lmlist[p2][1], self.lmlist[p2][2]
            
            cv2.circle(frame, (x1, y1), p1, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), p1, (255, 0, 255), cv2.FILLED) 

            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)   

            cx = (x1+x2) // 2
            cy = (y1+y2) // 2

            length = math.sqrt((x1-x2)**2 + (y1-y2)**2)

            if length < 50:
                cv2.circle(frame, (cx, cy), p1, (0, 255, 100), cv2.FILLED) 
            else:
                cv2.circle(frame, (cx, cy), p1, (255, 0, 255), cv2.FILLED) 

        return length, frame, [x1, y1, x2, y2, cx, cy]
        

          

def main():
    # Start webcam capture
    cap = cv2.VideoCapture(0)
    detector = HandTracker()

    while True:
        ret, frame = cap.read()  # Read the frame from the webcam
        if not ret:
            break

        # Find and mark the hands in the frame
        frame = detector.find_hands(frame)
        lmlist = detector.find_position(frame)

        distance = detector.findDistance(frame=frame, p1=8, p2=12)

        print(type(distance))

        previousTime = 0

        currentTime = time.time()
        fps = 1 / (currentTime-previousTime)
        previousTime = currentTime
        
        # Displaying FPS on the frame
        cv2.putText(frame, f"FPS : {int(fps)}", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)

        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) == ord('e'):
            break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
