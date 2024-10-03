import cv2
import numpy as np

# Global variables
points = []
drawing = False
area_calculated = False

def draw_polygon(event, x, y, flags, param):
    global points, drawing, area_calculated
    
    if event == cv2.EVENT_LBUTTONDOWN:
        # Start drawing when left mouse button is pressed
        drawing = True
        points.append((x, y))
        area_calculated = False

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            # Continue adding points as the mouse moves
            if len(points) > 0:
                # Draw a line from the last point to the current mouse position
                cv2.line(param, points[-1], (x, y), (0, 255, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        # Stop drawing when the left mouse button is released
        drawing = False
        points.append((x, y))

    elif event == cv2.EVENT_RBUTTONDOWN:
        # Right click to finalize and calculate the area
        if len(points) > 2:  # Need at least 3 points to form a polygon
            area_calculated = True

# Capture video from the default camera
cap = cv2.VideoCapture(0)

# Set up mouse callback
cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame', draw_polygon, param=cap)

while True:
    # Read the frame from the camera
    ret, frame = cap.read()
    
    # Draw the current polygon
    if len(points) > 1:
        for i in range(1, len(points)):
            cv2.line(frame, points[i - 1], points[i], (0, 255, 0), 2)
    
    if area_calculated:
        # Complete the polygon by connecting the last point to the first
        cv2.line(frame, points[-1], points[0], (0, 255, 0), 2)
        
        # Calculate the area of the polygon
        polygon = np.array(points)
        area = cv2.contourArea(polygon)
        
        # Display the area on the frame
        cv2.putText(frame, f'Area: {int(area)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        # Reset points and flag after displaying the area
        points = []
        area_calculated = False
    
    # Display the resulting frame
    cv2.imshow('Frame', frame)
    
    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
