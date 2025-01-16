import cv2
import numpy as np

def detect_color(frame, color_lower, color_upper):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, color_lower, color_upper)
    return mask

def count_color_pixels(image, color_channel):
    height, width, _ = image.shape
    left_half = image[:, :width // 2, color_channel]
    right_half = image[:, width // 2:, color_channel]
    
    left_count = np.count_nonzero(left_half)
    right_count = np.count_nonzero(right_half)

    return left_count, right_count

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

    # left_white = cv2.countNonZero(left_region)
    # right_white = cv2.countNonZero(right_region)

    # Detect green color
    green_lower = np.array([35, 100, 100])
    green_upper = np.array([85, 255, 255])
    green_mask = detect_color(frame, green_lower, green_upper)

    # Detect red color
    red_lower = np.array([0, 100, 100])
    red_upper = np.array([10, 255, 255])
    red_mask = detect_color(frame, red_lower, red_upper)

    # Detect blue color
    blue_lower = np.array([100, 185, 50])
    blue_upper = np.array([130, 255, 255])
    blue_mask = detect_color(frame, blue_lower, blue_upper)

    # Create a new image with edges in white, greens in green, and reds in red
    combined = np.zeros((height, width, 3), dtype=np.uint8)
    combined[:, :, 0] = np.where(red_mask > 0, 5, combined[:, :, 0])  # Red
    combined[:, :, 1] = np.where(red_mask > 0, 5, combined[:, :, 1])
    combined[:, :, 2] = np.where(red_mask > 0, 255, combined[:, :, 2])

    combined[:, :, 0] = np.where(green_mask > 0, 22, combined[:, :, 0])  # Green
    combined[:, :, 1] = np.where(green_mask > 0, 115, combined[:, :, 1])
    combined[:, :, 2] = np.where(green_mask > 0, 25, combined[:, :, 2])

    combined[:, :, 0] = np.where(blue_mask > 0, 255, combined[:, :, 0])  # Blue
    combined[:, :, 1] = np.where(blue_mask > 0, 0, combined[:, :, 1])
    combined[:, :, 2] = np.where(blue_mask > 0, 0, combined[:, :, 2])

    combined[:, :, 0] = np.where(edges > 0, 255, combined[:, :, 0])  # White
    combined[:, :, 1] = np.where(edges > 0, 255, combined[:, :, 1])
    combined[:, :, 2] = np.where(edges > 0, 255, combined[:, :, 2])

    #  counting pixels of red and green in the combined window
    red_left, red_right = count_color_pixels(combined, 2)  # Red channel
    green_left, green_right = count_color_pixels(combined, 1)  # Green channel

    cv2.imshow("Frame", frame)
    cv2.imshow("Combined", combined)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()