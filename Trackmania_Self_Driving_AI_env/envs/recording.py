import cv2
import numpy as np
from PIL import Image, ImageGrab

def process_img(printscreen):
    processed_img = cv2.cvtColor(printscreen, cv2.COLOR_RGB2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    gauss_img = cv2.GaussianBlur(processed_img,(5, 5), 0)
    return gauss_img

def count_pixels(img, angle, start_point, color_range, step_size):
    angle = np.radians(angle)
    grad = np.tan(angle)
    
    distance = 0
    current_point = (0, 0)

    for i in range(0, 321):
        if (current_point[0] >= 0 and current_point[1] >= 0) and all(img[current_point[1], current_point[0]] >= color_range[0]) and all(img[current_point[1], current_point[0]] <= color_range[1]):
            return distance
        current_point = np.array([np.abs(start_point[0] + i * step_size),
                                int(start_point[1] - grad * (i))])
        
        distance += 1

    return 10000

def on_grass(img, lower_bounds, upper_bounds):
    half_img = img[260:, :, :]

    half_img = cv2.cvtColor(half_img, cv2.COLOR_BGR2RGB)
    half_img = cv2.GaussianBlur(half_img,(31, 31), 10)

    mask1 = np.logical_and(half_img[..., 0] >= lower_bounds[0],
                           half_img[..., 0] <= upper_bounds[0])
    mask2 = np.logical_and(half_img[..., 1] >= lower_bounds[1],
                           half_img[..., 1] <= upper_bounds[1])
    mask3 = np.logical_and(half_img[..., 2] >= lower_bounds[2],
                           half_img[..., 2] <= upper_bounds[2])
    if np.all(mask1) and \
        np.all(mask2) and \
            np.all(mask3):
        return True
    return False

def screen_record():
    while(True):
        printscreen = np.array(ImageGrab.grab(bbox=(0, 40, 640, 519)))
        cv2.imshow('Trackmania Self Driving car', printscreen)
        print(on_grass(printscreen, ([12, 42, 27]), ([46, 120, 81])))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    screen_record()