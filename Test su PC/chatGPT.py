import cv2
import numpy as np

# Callback function for the trackbar
def on_trackbar(val):
    pass

# Initialize the camera
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Error opening the camera.")
    exit()

# Grid dimensions
cell_num = 20

# Create trackbars
cv2.namedWindow("Trackbars")
cv2.createTrackbar("Lower", "Trackbars", 0, 255, on_trackbar)
cv2.createTrackbar("Higher", "Trackbars", 0, 255, on_trackbar)

while True:
    # Read a frame from the camera
    ret, frame = camera.read()
    if not ret:
        print("Error reading the frame.")
        break

    # Convert to grayscale and apply thresholding
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    lower = cv2.getTrackbarPos('Lower', 'Trackbars')
    higher = cv2.getTrackbarPos('Higher', 'Trackbars')
    _, binary = cv2.threshold(gray, lower, higher, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(binary, 50, 150)

    # Get frame dimensions
    height, width = edges.shape
    square_height = height // cell_num
    square_width = width // cell_num

    # Initialize counters
    left_counts = {'red': 0, 'green': 0, 'black': 0}
    right_counts = {'red': 0, 'green': 0, 'black': 0}

    # Analyze each cell
    for i in range(cell_num):
        for j in range(cell_num):
            # Define cell boundaries
            x_start = j * square_width
            y_start = i * square_height
            x_end = x_start + square_width
            y_end = y_start + square_height

            # Extract the cell
            cell = frame[y_start:y_end, x_start:x_end]

            # Check for color presence
            cell_hsv = cv2.cvtColor(cell, cv2.COLOR_BGR2HSV)
            red_mask = cv2.inRange(cell_hsv, (0, 50, 50), (10, 255, 255))
            green_mask = cv2.inRange(cell_hsv, (35, 50, 50), (85, 255, 255))
            black_mask = cv2.inRange(cell_hsv, (0, 0, 0), (180, 255, 50))

            if cv2.countNonZero(red_mask) > 0:
                color = 'red'
                cv2.rectangle(edges, (x_start, y_start), (x_end, y_end), (0, 0, 255), -1)
            elif cv2.countNonZero(green_mask) > 0:
                color = 'green'
                cv2.rectangle(edges, (x_start, y_start), (x_end, y_end), (0, 255, 0), -1)
            elif cv2.countNonZero(black_mask) > 0:
                color = 'black'
                cv2.rectangle(edges, (x_start, y_start), (x_end, y_end), (0, 0, 0), -1)
            else:
                continue

            # Update counters
            if x_start < width // 2:
                left_counts[color] += 1
            else:
                right_counts[color] += 1

    # Display counters
    print(f"Left counts: {left_counts}")
    print(f"Right counts: {right_counts}")

    # Show the frames
    cv2.imshow("Frame", frame)
    cv2.imshow("Edges", edges)

    # Exit with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
camera.release()
cv2.destroyAllWindows()
