import cv2
import numpy as np
import serial
import time
import json
# Inizializzazione parametri PID
kp = 0.5  # Proporzionale
ki = 0.1  # Integrale
kd = 0.2  # Derivativo
integral = 0
previous_error = 0

# Funzione per calcolare il centroide
def calculate_centroid(region):
    contours, _ = cv2.findContours(region, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            return cx
    return None

# Funzione per calcolare l'angolo di inclinazione
def calculate_line_angle(region):
    contours, _ = cv2.findContours(region, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        points = largest_contour.reshape(-1, 2)
        [vx, vy, _, _] = cv2.fitLine(points, cv2.DIST_L2, 0, 0.01, 0.01)
        angle = np.arctan2(vy, vx) * 180 / np.pi
        return angle
    return None

# Funzione per controllare i motori
def control_motors(output):
    if output > 0:
        print(f"Gira a destra con intensità: {output}")
        # Aggiungi qui il codice per controllare i motori verso destra
    elif output < 0:
        print(f"Gira a sinistra con intensità: {abs(output)}")
        # Aggiungi qui il codice per controllare i motori verso sinistra
    else:
        print("Vai dritto")
        # Aggiungi qui il codice per andare dritto

# Inizializzazione videocamera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Ridimensiona il frame per migliorare la velocità
    frame = cv2.resize(frame, (640, 480))

    # Converti in scala di grigi e applica una soglia binaria
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

    # Considera solo un ROI nella parte inferiore del frame
    height, width = binary.shape
    roi = binary[height // 2:, :]

    # Calcola il centroide
    cx = calculate_centroid(roi)

    # Calcola l'angolo di inclinazione
    angle = calculate_line_angle(roi)

    if cx is not None:
        # Calcola l'errore (distanza del centroide dal centro del frame)
        error = width // 2 - cx

        # Controllo PID
        integral += error
        derivative = error - previous_error
        output = kp * error + ki * integral + kd * derivative
        previous_error = error

        # Controlla i motori
        control_motors(output)

        # Disegna sul frame
        cv2.circle(frame, (cx, height // 2 + height // 4), 5, (0, 255, 0), -1)
        if angle is not None:
            cv2.putText(frame, f"Angolo: {angle:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Mostra il frame elaborato
    cv2.imshow("Frame", frame)
    cv2.imshow("Binary", binary)

    # Esci premendo 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()