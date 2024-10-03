import cv2
import mediapipe as mp
import numpy as np
import detector_hand_face_module as dhm
import os

cap = cv2.VideoCapture(0)
detector = dhm.HandTracker()


directiry = 'fingers_images'
mylist = os.listdir(directiry)


list_links = []

for image in mylist:
    images= f'{directiry}/{image}'
    list_links.append(images)

print(list_links)


tips = [4, 8, 12, 16, 20]

while True:

    ret, image = cap.read()
    mylist, _ = detector.find_position(image, drow=False)

    image = detector.find_hands(image)

    open_or_close = []

    if len(mylist) != 0:

        
        if mylist[tips[0]][1] > mylist[tips[0]-1][1]:
            open_or_close.append(1)
        else:
            open_or_close.append(0)


        for id in range(1, 5):
            if mylist[tips[id]][2] < mylist[tips[id]-2][2]:
                open_or_close.append(1)
            else:
                open_or_close.append(0)
    
    print(open_or_close)

    countor = 0

    if len(open_or_close) != 0:
        if open_or_close[0] == 1:
            overly_image = cv2.imread(list_links[5])
            overly_image = cv2.resize(overly_image, (200, 200))
            image[0:200, 0:200] = overly_image 
        elif open_or_close[1] == 1:
            overly_image = cv2.imread(list_links[1])
            overly_image = cv2.resize(overly_image, (200, 200))
            image[0:200, 0:200] = overly_image


            if open_or_close[2] == 1:
                overly_image = cv2.imread(list_links[2])
                overly_image = cv2.resize(overly_image, (200, 200))
                image[0:200, 0:200] = overly_image

                if open_or_close[3] == 1:
                    overly_image = cv2.imread(list_links[3])
                    overly_image = cv2.resize(overly_image, (200, 200))
                    image[0:200, 0:200] = overly_image

                    if open_or_close[4] == 1:
                        overly_image = cv2.imread(list_links[4])
                        overly_image = cv2.resize(overly_image, (200, 200))
                        image[0:200, 0:200] = overly_image

        else:
            overly_image = cv2.imread(list_links[0])
            overly_image = cv2.resize(overly_image, (200, 200))
            image[0:200, 0:200] = overly_image

    # calculate the number of fingers ........
    
    for count in range(len(open_or_close)):
        if len(open_or_close) != 0:
            if open_or_close[count] == 1:
                countor += 1
    
    print(countor)

    cv2.putText(image, f'The Number Of Fingers:{countor}', (10, 430), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)

    cv2.imshow('my freme', image)

    if cv2.waitKey(1) == ord('e'):
        break

cap.release()
cv2.destroyAllWindows()