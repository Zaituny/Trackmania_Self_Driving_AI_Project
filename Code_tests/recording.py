import cv2
import numpy as np
from PIL import Image, ImageGrab
import time

time.sleep(2)

def process_img(printscreen):
    processed_img = cv2.cvtColor(printscreen, cv2.COLOR_RGB2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    gauss_img = cv2.GaussianBlur(processed_img,(5, 5), 0)
    return gauss_img

def count_pixels(img, angle, start_point, color_range,step_size):
    grad = np.tan(angle)
    c = grad * start_point[0] - start_point[1]

    current_point = start_point
    distance = 0

    while (0 <= current_point[0] < img.shape[1]) and (0 <= current_point[1] < img.shape[0]) and (distance <= 519):
        if all(img[current_point[1], current_point[0]] >= color_range[0]) and all(img[current_point[1], current_point[0]] <= color_range[1]):
            cv2.line(img, start_point, current_point, (255, 0, 0),2)
            return distance

        current_point = np.array([current_point[0] + step_size, int(grad * (current_point[0] + step_size) - c)])
        distance += 1

    return None
    
def screen_record():
    while(True):
        printscreen = np.array(ImageGrab.grab(bbox=(0, 40, 640, 519)))
        #processed_img = process_img(printscreen)
        #printscreen = cv2.cvtColor(printscreen, cv2.COLOR_RGB2GRAY)

        print(count_pixels(printscreen, -15, (320, 478), ((10, 15, 30), (50, 55, 70)), -1))
        print(count_pixels(printscreen, -30, (320, 478), ((10, 15, 30), (50, 55, 70)), -1))
        print(count_pixels(printscreen, -45, (320, 478), ((10, 15, 30), (50, 55, 70)), -1))
        print(count_pixels(printscreen, -60, (320, 478), ((10, 15, 30), (50, 55, 70)), -1))
        print(count_pixels(printscreen, -75, (320, 478), ((10, 15, 30), (50, 55, 70)), -1))
        print(count_pixels(printscreen,  75, (320, 478), ((10, 15, 30), (50, 55, 70)),  1))
        print(count_pixels(printscreen,  60, (320, 478), ((10, 15, 30), (50, 55, 70)),  1))
        print(count_pixels(printscreen,  45, (320, 478), ((10, 15, 30), (50, 55, 70)),  1))
        print(count_pixels(printscreen,  30, (320, 478), ((10, 15, 30), (50, 55, 70)),  1))
        print(count_pixels(printscreen,  15, (320, 478), ((10, 15, 30), (50, 55, 70)),  1))        
        
        cv2.imshow('Trackmania Self Driving car', printscreen)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

screen_record()