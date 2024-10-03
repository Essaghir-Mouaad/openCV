import cv2
import numpy as np

image = cv2.imread('C:/Users/mouad/Pictures/Screenshots/circle.png', )
image = cv2.resize(image, (0, 0), fx=.7, fy=.7)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
# corners = np.int0(corners)

# for i in corners:
# 	x, y = i.ravel()
# 	cv2.circle(image, (x, y), 4, (255, 0, 0), -1)

# print(corners)
# for i in range(len(corners)) :
# 	for j in range(i+1, len(corners)):
# 		cornersx = tuple(corners[i][0])
# 		cornersy = tuple(corners[j][0])
# 		color = tuple(np.random.randint(0, 255, size=3).tolist())
# 		cv2.line(image, cornersx, cornersy, color, 1)

# cv2.imshow('image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()




canny = cv2.Canny(image, 123, 200)

ret, thresh = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY)

conto, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(image, conto,-1, tuple(np.random.randint(0, 255, size=3).tolist()), 2)

i = 1
total_area = 0

for contour in conto :
	area = cv2.contourArea(contour)
	print(f'the area of the contour{i} is {area} pexile squer')
	total_area += area
	i+=1

print(f'the total area is : {total_area}')

print(len(conto))

cv2.imshow('the contor image', image)
cv2.waitKey(0)


x_array = []
y_array = []

# for i in conto[0]:
#     x, y = i.ravel()
#     x_array.append(x)
#     y_array.append(y)
# print(x_array)

def calculate_Contour_area(conto):
	total_area = 0
	x_array = []
	y_array = []

	for j in range((len(conto)-1)):
		for i in conto[j]:
		    x, y = i.ravel()
		    x_array.append(x)
		    y_array.append(y)

		x = x_array[(len(x_array)-1)] * y_array[0]
		y = y_array[(len(y_array)-1)] * x_array[0]


		for i in range(len(y_array)-1):
			x += x_array[i] * y_array[i+1]
			y += y_array[i] * x_array[i+1]
			area = 1/2 * abs(x - y)

		total_area += area
	
	print(f'the area of this contour using a manually way is {total_area} meter squer')

calculate_Contour_area(conto)
# print(x_array)
# print(y_array)