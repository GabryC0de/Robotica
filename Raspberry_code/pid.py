import cv2
import gpiozero
import serial
import time

def pid(black_left, black_right):
    kp = 2.8
    ki = 0.02
    kd = 0.28
    
    error = black_left - black_right
    integral += error
    if error <= 1:
        integral = 0
    derivative = error - previous_error
    
    previous_error = error
    
    deviation_rate = (error * kp) + (integral * ki) + (derivative * kd)
    
    return int(deviation_rate)

# try:
#     while True:
#         # Get user input
#         user_input = input("Enter command: ").strip()
#         if user_input == 'q':
#             print("Exiting...")
#             break
#         if user_input in ['r', 'l']:
#             arduino.write(user_input.encode())  # Send the command to Arduino            
#             # Wait for Arduino's response
#             response = arduino.readline().decode('utf-8').strip()
#             if response:
#                 print(f"Received from Arduino: {response}")