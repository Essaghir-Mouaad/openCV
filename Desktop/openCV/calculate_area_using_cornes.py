import cv2 as cv
import numpy as np
import matplotlib

image = cv.imread('C:/Users/mouad/Pictures/Screenshots/circle.png')

image = cv.resize(image, (0, 0), fx=.8, fy=.7)

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

canny = cv.Canny(image, 125, 200)

_, thresh = cv.threshold(gray, 125, 200, cv.THRESH_BINARY)

corners = cv.goodFeaturesToTrack(canny, 1000, 0.01, 10)
corners = np.int0(corners)

color = tuple(np.random.randint(0, 255, size=3).tolist())

x_array = []
y_array = []

for i in corners:
	x, y = i.ravel()
	cv.circle(image, (x, y), 2, color, -1)
	x_array.append(x)
	y_array.append(y)

x = x_array[(len(x_array)-1)] * y_array[0]
y = y_array[(len(y_array)-1)] * x_array[0]


for i in range(len(y_array)-1):
	x += x_array[i] * y_array[i+1]
	y += y_array[i] * x_array[i+1]
	area = 1/2 * abs(x - y)

print(f'the area of this geometry is : {area}')

cv.imshow('my image', canny)
cv.waitKey(0)
cv.destroyAllWindows()
