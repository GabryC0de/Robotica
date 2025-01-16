import cv2

# Callback function for the trackbar (called when slider value changes)
def on_trackbar(val):
    pass



# creo trackbars per effetture le misure
def createTrackbars():
    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("Lower", "Trackbars", 0, 255, on_trackbar)
    cv2.createTrackbar("Higher", "Trackbars", 0, 255, on_trackbar)

    cv2.createTrackbar("Lower Canny", "Trackbars", 0, 255, on_trackbar)
    cv2.createTrackbar("Higher Canny", "Trackbars", 0, 255, on_trackbar)

    cv2.namedWindow("Red")
    cv2.namedWindow("Green")
    cv2.namedWindow("Black")
    # red
    cv2.createTrackbar("Red Hue Min", "Red", 0, 179, on_trackbar);
    cv2.createTrackbar("Red Hue Max", "Red", 0, 179, on_trackbar);
    cv2.createTrackbar("Red Sat Min", "Red", 0, 255, on_trackbar);
    cv2.createTrackbar("Red Sat Max", "Red", 0, 255, on_trackbar);
    cv2.createTrackbar("Red Val Min", "Red", 0, 255, on_trackbar);
    cv2.createTrackbar("Red Val Max", "Red", 0, 255, on_trackbar);
    # green
    cv2.createTrackbar("Green Hue Min", "Green", 0, 179, on_trackbar);
    cv2.createTrackbar("Green Hue Max", "Green", 0, 179, on_trackbar);
    cv2.createTrackbar("Green Sat Min", "Green", 0, 255, on_trackbar);
    cv2.createTrackbar("Green Sat Max", "Green", 0, 255, on_trackbar);
    cv2.createTrackbar("Green Val Min", "Green", 0, 255, on_trackbar);
    cv2.createTrackbar("Green Val Max", "Green", 0, 255, on_trackbar);
    # black
    cv2.createTrackbar("Black Hue Min", "Black", 0, 179, on_trackbar);
    cv2.createTrackbar("Black Hue Max", "Black", 0, 179, on_trackbar);
    cv2.createTrackbar("Black Sat Min", "Black", 0, 255, on_trackbar);
    cv2.createTrackbar("Black Sat Max", "Black", 0, 255, on_trackbar);
    cv2.createTrackbar("Black Val Min", "Black", 0, 255, on_trackbar);
    cv2.createTrackbar("Black Val Max", "Black", 0, 255, on_trackbar);



def readTrackbarsPosition():
    red_hue_min = cv2.getTrackbarPos('Red Hue Min', 'Red')
    red_hue_max = cv2.getTrackbarPos('Red Hue Max', 'Red')
    red_sat_min = cv2.getTrackbarPos('Red Sat Min', 'Red')
    red_sat_max = cv2.getTrackbarPos('Red Sat Max', 'Red')
    red_val_min = cv2.getTrackbarPos('Red Val Min', 'Red')
    red_val_max = cv2.getTrackbarPos('Red Val Max', 'Red')

    green_hue_min = cv2.getTrackbarPos('Green Hue Min', 'Green')
    green_hue_max = cv2.getTrackbarPos('Green Hue Max', 'Green')
    green_sat_min = cv2.getTrackbarPos('Green Sat Min', 'Green')
    green_sat_max = cv2.getTrackbarPos('Green Sat Max', 'Green')
    green_val_min = cv2.getTrackbarPos('Green Val Min', 'Green')
    green_val_max = cv2.getTrackbarPos('Green Val Max', 'Green')

    black_hue_min = cv2.getTrackbarPos('Black Hue Min', 'Black')
    black_hue_max = cv2.getTrackbarPos('Black Hue Max', 'Black')
    black_sat_min = cv2.getTrackbarPos('Black Sat Min', 'Black')
    black_sat_max = cv2.getTrackbarPos('Black Sat Max', 'Black')
    black_val_min = cv2.getTrackbarPos('Black Val Min', 'Black')
    black_val_max = cv2.getTrackbarPos('Black Val Max', 'Black')
    
    lower = cv2.getTrackbarPos('Lower', 'Trackbars')
    higher = cv2.getTrackbarPos('Higher', 'Trackbars')
    lower_canny = cv2.getTrackbarPos('Lower Canny', 'Trackbars')
    higher_canny = cv2.getTrackbarPos('Higher Canny', 'Trackbars')
    return {
        "red": [
            red_hue_min, 
            red_hue_max, 
            red_sat_min, 
            red_sat_max, 
            red_val_min, 
            red_val_max
            ],
        "green": [
            green_hue_min, 
            green_hue_max, 
            green_sat_min, 
            green_sat_max, 
            green_val_min, 
            green_val_max            
        ],
        "black": [
            black_hue_min, 
            black_hue_max, 
            black_sat_min, 
            black_sat_max, 
            black_val_min, 
            black_val_max            
        ],
        "edges": [
            lower,
            higher,
        ],
        "canny": [
            lower_canny,
            higher_canny
        ]
    }
