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