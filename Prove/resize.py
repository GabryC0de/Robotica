import cv2

# Open a video capture
cap = cv2.VideoCapture(0)  # 0 for the default camera

if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Get the dimensions of the frame
    height, width, _ = frame.shape

    # Calculate the ROI (Region of Interest)
    # Focus on the middle area: cut away a third from each side
    cut_width = width // 3  # A third of the width
    x_start = cut_width  # Start of the focused area
    x_end = width - cut_width  # End of the focused area
    focused_frame = frame[:, x_start:x_end]  # Crop the frame horizontally

    # Display the original and cropped frames
    cv2.imshow("Original Frame", frame)
    cv2.imshow("Focused Frame", focused_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()
