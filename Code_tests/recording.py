import cv2
import numpy as np
from PIL import Image, ImageGrab
from keyboard import PressKey, ReleaseKey, UP, DOWN, RIGHT,LEFT
import time

time.sleep(2)

# def screen_record():
#   #  PressKey(UP)
#     while(True):
#                                                          #width,height                  
#         printscreen =  np.array(ImageGrab.grab(bbox=(0,40,800,640)))
#         processed_img = cv2.cvtColor(printscreen, cv2.COLOR_RGB2GRAY)
#         processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
#         cv2.imshow('window',processed_img)
#         print(processed_img)
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             cv2.destroyAllWindows()
#             break


# screen_record()

def draw_lines(img):
    lines = cv2.HoughLinesP(img, 1, np.pi/180, 180, np.array([]), 250, 7)
    if lines is not None:
        for line in lines:
            coords = line[0]
            cv2.line(img, (coords[0],coords[1]), (coords[2],coords[3]),(255, 255, 255), 2)
    return

def process_img(printscreen):
    processed_img = cv2.cvtColor(printscreen, cv2.COLOR_RGB2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    gauss_img = cv2.GaussianBlur(processed_img,(5, 5), 0)
    return gauss_img

def roi(img):
    vertices = np.array([[14,273],[259,219],[496,219],[799,251],[801,496],[677,494],[518,309],[269,311],[134,504],[7,500]])
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, [vertices], 255)
    masked_img = cv2.bitwise_and(img, mask)
    return masked_img

def screen_record():
    while(True):
        printscreen = np.array(ImageGrab.grab(bbox=(0,45,800,640)))
        processed_img = process_img(printscreen)
        masked_img = roi(processed_img)
        draw_lines(masked_img)
        cv2.imshow('Trackmania Self Driving car',masked_img)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

screen_record()