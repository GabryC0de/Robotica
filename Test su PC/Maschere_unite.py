import cv2
import numpy as np
import trackBars

# Inizializza la telecamera
camera = cv2.VideoCapture(1)

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

print(int(square_height) * int(square_width))

trackBars.createTrackbars()

while True:
    # Leggi un frame dalla telecamera
    ret, frame = camera.read() #ret = boolean, lettura riuscita. frame = frame letto
    if not ret:
        print("Errore nella lettura del frame.")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

    # red_values = trackBars.readTrackbarsPosition()["red"]
    # green_values = trackBars.readTrackbarsPosition()["green"]
    black_values = trackBars.readTrackbarsPosition()["black"]
    # print(black_values)

    _, binary = cv2.threshold(gray, 50, 120, cv2.THRESH_BINARY_INV)
    # _, binary = cv2.threshold(gray, lower, higher, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(binary, 50, 150)
    # edges = cv2.Canny(binary, lower_canny, higher_canny)

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
            cv2.rectangle(edges, (x_start, y_start), (x_end, y_end), (255, 255, 255), 1)

            # chat gpt
            cell = frame[y_start:y_end, x_start:x_end]

            # controllo la presenza di colori
            cell_hsv = cv2.cvtColor(cell, cv2.COLOR_BGR2HSV)
            # red_mask = cv2.inRange(cell_hsv, (red_values[0], red_values[2], red_values[4]), (red_values[1], red_values[3], red_values[5]))
            red_mask = cv2.inRange(cell_hsv, (0, 0, 0), (0, 0, 0))
            # green_mask = cv2.inRange(cell_hsv, (green_values[0], green_values[2], green_values[4]), (green_values[1], green_values[3], green_values[5])
            green_mask = cv2.inRange(cell_hsv, (46, 201, 56), (89, 255, 121))
            black_mask = cv2.inRange(cell_hsv, (black_values[0], black_values[2], black_values[4]), (black_values[1], black_values[3], black_values[5]))
            # black_mask = cv2.inRange(cell_hsv, (75, 60, 10), (180, 110, 110))

            # if cv2.countNonZero(red_mask) > (768/4)*3:
            if cv2.countNonZero(red_mask) > 0:
                color = 'red'
                cv2.rectangle(edges, (x_start, y_start), (x_end, y_end), (0, 0, 255), -1)
            # elif cv2.countNonZero(green_mask) > (768/4)*3:
            elif cv2.countNonZero(green_mask) > 0:
                color = 'green'
                cv2.rectangle(edges, (x_start, y_start), (x_end, y_end), (0, 255, 0), -1)
            # elif cv2.countNonZero(black_mask) > (768/4)*3:
            elif cv2.countNonZero(black_mask) > 0:
                color = 'black'
                cv2.rectangle(edges, (x_start, y_start), (x_end, y_end), (255, 255, 255), -1)
            else:
                continue

            # Update counters
            if x_start < width // 2:
                left_counts[color] += 1
            else:
                right_counts[color] += 1


    # Display counters
    print(f"Left counts: {left_counts['black']}, Right counts: {right_counts['black']}")

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