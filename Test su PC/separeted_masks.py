import cv2
import numpy as np

def detect_color(frame, color_lower, color_upper):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, color_lower, color_upper)
    return mask

cap = cv2.VideoCapture(0)  # Capture video from the camera

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(binary, 50, 150)

    height, width = edges.shape
    left_region = edges[:, :width//2]
    right_region = edges[:, width//2:]

    left_white = cv2.countNonZero(left_region)
    right_white = cv2.countNonZero(right_region)

    # Detect green color
    green_lower = np.array([35, 100, 100])
    green_upper = np.array([85, 255, 255])
    green_mask = detect_color(frame, green_lower, green_upper)

    green_left_region = green_mask[:, :width//2]
    green_right_region = green_mask[:, width//2:]

    green_left = cv2.countNonZero(green_left_region)
    green_right = cv2.countNonZero(green_right_region)

    # Detect Red Color
    red_lower = np.array([0, 100, 100])
    red_upper = np.array([10, 255, 255])
    red_mask = detect_color(frame, red_lower, red_upper)

    red_left_region = red_mask[:, :width//2]
    red_right_region = red_mask[:, width//2:]

    red_left = cv2.countNonZero(red_left_region)
    red_right = cv2.countNonZero(red_right_region)

    cv2.imshow("Frame", frame)
    cv2.imshow("Edges", edges)
    cv2.imshow("Green Mask", green_mask)
    cv2.imshow("Red Mask", red_mask)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()