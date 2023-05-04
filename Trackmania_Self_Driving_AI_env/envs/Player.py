from tminterface.interface import TMInterface
from tminterface.client import Client, run_client
from PIL import ImageGrab
import tensorflow as tf 
from keras.layers.core import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers import concatenate
from keras.utils.vis_utils import plot_model
from keras.layers import Input
from keras.models import Model
import numpy as np
import pyvjoy
import pyautogui
import pydirectinput

j = pyvjoy.VJoyDevice(1)

input_img = Input(shape=(224, 224, 3), name='img_input')
### 1st layer
layer_1 = Conv2D(10, (1,1), padding='same', activation='relu')(input_img)
layer_1 = Conv2D(10, (3,3), padding='same', activation='relu')(layer_1)

layer_2 = Conv2D(10, (1,1), padding='same', activation='relu')(input_img)
layer_2 = Conv2D(10, (5,5), padding='same', activation='relu')(layer_2)

layer_3 = MaxPooling2D((3,3), strides=(1,1), padding='same')(input_img)
layer_3 = Conv2D(10, (1,1), padding='same', activation='relu')(layer_3)

mid_1 = concatenate([layer_1, layer_2, layer_3], axis = 3)
merged = Dropout(0.5)(mid_1)

flat_1 = Flatten()(merged)

classification_output = Dense(1, activation='sigmoid', name='classification_output')(flat_1)
Dense_1 = Dense(16, activation=tf.keras.layers.LeakyReLU(alpha=0.01))(flat_1)
linear_output = Dense(1, activation='linear', name='linear_output')(Dense_1)

model = Model(inputs=[input_img], outputs=[classification_output, linear_output])

model.load_weights('C:\\Users\\Mohamed Ali\Documents\\Semester_6\\Artificial_Intelligence\\Project\\Trackmania_Self_Driving_AI_env\\Trackmania_Self_Driving_AI_env\\envs\\checkpoints\\model_weights.h5')

while True:
    screen = np.array(ImageGrab.grab(bbox=(0, 40, 640, 519)))
    screen.resize(224, 224, 3)
    screen = screen.reshape(1, 224, 224, 3)
    accelrate_break, steer = model.predict(screen)
    if not int(accelrate_break[0][0]):
        pydirectinput.press('up')
        j.set_axis(pyvjoy.HID_USAGE_X, hex(int(np.interp(steer[0][0], [-1, 1], [1, 32768]))))
    elif int(accelrate_break[0][0]):
        pydirectinput.press('down')
        j.set_axis(pyvjoy.HID_USAGE_X, hex(int(np.interp(steer[0][0], [-1, 1], [1, 32768]))))