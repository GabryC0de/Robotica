import cv2
# import numpy as np
import serial
import time
import json

# Inizializza la telecamera
camera = cv2.VideoCapture(0)# Configure the serial connection
arduino = serial.Serial('COM7', 9600, timeout=1)  # Adjust port if needed
time.sleep(2)  # Wait for the connection to initialize

if not camera.isOpened():
    print("Errore nell'aprire la telecamera.")
    exit()

# Dimensioni della griglia
cell_num = 40  # numero di righe e colonne desiderato
# Ottieni dimensioni del frame
retProva, frameProva = camera.read() #ret = boolean, lettura riuscita. frame = frame letto
height, width, _ = frameProva.shape
square_height = height / cell_num
square_width = width / cell_num

integral = 0
derivative = 0
previous_error = 0

while True:
    # Leggi un frame dalla telecamera
    ret, frame = camera.read() #ret = boolean, lettura riuscita. frame = frame letto
    if not ret:
        print("Errore nella lettura del frame.")
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 50, 120, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(binary, 50, 150)

    # Ottieni dimensioni del frame
    height, width = edges.shape

    edges_left_half = edges[:, :width // 2]
    edges_right_half = edges[:, width // 2:]

    square_height = height / cell_num
    square_width = width / cell_num

    # Initialize counters
    left_counts = {'red': 0, 'green': 0, 'black': 0}
    right_counts = {'red': 0, 'green': 0, 'black': 0}

    cv2.line(edges, (width // 2, 0), (width // 2, height), (255, 0, 0), 2)
    # Disegna la griglia sull'immagine
    for y in range(0, height, int(square_height)):
        for x in range(0, width, int(square_width)):
            # Define cell boundaries
            x_start = x
            y_start = y
            x_end = x + int(square_width)
            y_end = y + int(square_height)
            # Disegna il rettangolo della cella
            #             frame, top-Left, bottom right, color, line thicknes
            cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 1) # chatGPT
            cv2.rectangle(edges, (x_start, y_start), (x_end, y_end), (0, 255, 0), 1)

            # chat gpt
            cell = frame[y_start:y_end, x_start:x_end]

            # controllo la presenza di colori
            cell_hsv = cv2.cvtColor(cell, cv2.COLOR_BGR2HSV)
            green_mask = cv2.inRange(cell_hsv, (46, 201, 56), (89, 255, 121))
            black_mask = cv2.inRange(cell_hsv, (39, 0, 0), (136, 248, 62))
            red_mask = cv2.inRange(cell_hsv, (0, 0, 0), (0, 0, 0))

            if cv2.countNonZero(red_mask) > (768/4)*3:
                color = 'red'
                cv2.rectangle(edges, (x_start, y_start), (x_end, y_end), (0, 0, 255), -1)
            elif cv2.countNonZero(green_mask) > (768/4)*3:
                color = 'green'
                cv2.rectangle(edges, (x_start, y_start), (x_end, y_end), (0, 255, 0), -1)
            # elif cv2.countNonZero(black_mask) > (768/4)*3: # metà pixer di un riquadro
            elif cv2.countNonZero(black_mask) > 0: # metà pixer di un riquadro
                color = 'black'
                cv2.rectangle(edges, (x_start, y_start), (x_end, y_end), (255, 255, 255), -1)
            else:
                continue

            # Update counters
            if x_start < width // 2:
                left_counts[color] += 1
            else:
                right_counts[color] += 1
    # double green
    if ((left_counts['green'] - right_counts['green']) in range(0, 5)):
        # direction, pwm left, pwm right
        values = {
            "direction":"back",
            #forward
            "PWM_L":255,
            #backwards
            "PWM_R":255,
            "time": 5
            }
        # Serialize the dictionary to a JSON string
        json_data = json.dumps(values)
        
        # Send the JSON string over serial
        arduino.write(f"g{json_data.encode('utf-8')}\n")     # also send a newline character as a delimiter
        
        if arduino.in_waiting > 0:  # Check if there's a response
            response = arduino.readline().decode('utf-8').strip()
            print(f"Arduino responded: {response}")
    # green detected on the left
    elif ((left_counts['green'] > right_counts['green']) and left_counts['green']) > 5:
        # direction, pwm left, pwm right
        values = {
            "direction":"left",
            "PWM_L":0,
            "PWM_R":255,
            "time": 5
            }
        # Serialize the dictionary to a JSON string
        json_data = json.dumps(values)
        # Send the JSON string over serial
        arduino.write(f"g{json_data.encode('utf-8')}\n")     # also send a newline character as a delimiter
        
        if arduino.in_waiting > 0:  # Check if there's a response
            response = arduino.readline().decode('utf-8').strip()
            print(f"Arduino responded: {response}")
    
    # green detected
    elif ((right_counts['green'] > left_counts['green']) and right_counts['green']) > 5:
        # direction, pwm left, pwm right
        values = {
            "direction":"right",
            "PWM_L":255,
            "PWM_R":0,
            "time": 5
            }
        # Serialize the dictionary to a JSON string
        json_data = json.dumps(values)
        
        # Send the JSON string over serial
        arduino.write(f"g{json_data.encode('utf-8')}\n")     # also send a newline character as a delimiter        


    # starting the P section
    kp = 1
    ki = 0
    kd = 0
    
    error = left_counts['black'] - right_counts['black']
    integral += error
    if error <= 10:
        integral = 0
    derivative = error - previous_error
    previous_error = error
    # calcolo deviazione del robot dal centro della linea
    deviation = (error * kp) + (integral * ki) + (derivative * kd)

    arduino.write(f"p{deviation}\n".encode('utf-8'))

    if arduino.in_waiting > 0:  # Check if there's a response
        response = arduino.readline().decode('utf-8').strip()
        print(f"Arduino responded: {response}")

    
    # Mostra il frame con la griglia
    cv2.imshow("Frame", frame)
    # Mostra i contorni con la griglia
    cv2.imshow("Edges", edges)

    # Esci con il tasto 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Rilascia le risorse
camera.release()
cv2.destroyAllWindows()
arduino.close()
