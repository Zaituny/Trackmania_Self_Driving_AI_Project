from tminterface.interface import TMInterface
from tminterface.client import Client, run_client 
import sys
import pandas as pd
import recording
from PIL import ImageGrab
import numpy as np
import multiprocessing
import concurrent.futures
df = pd.DataFrame(columns=['img',
                           'left_15',
                           'left_30',
                           'left_45',
                           'left_60',
                           'left_75',
                           'right_15',
                           'right_30',
                           'right_45',
                           'right_60',
                           'right_75',
                           'speed',
                           'label'])

screens_list = []
states_list = []
time = []
curr_list = []

class MainClient(Client):

    def __init__(self, screens_list, states_list, time, curr_list) -> None:
        super(MainClient, self).__init__()
        self.prev = np.array([False, False, False, False])
        self.curr = np.array([False, False, False, False])
        self.screens_list = screens_list
        self.states_list = states_list
        self.time = time
        self.curr_list = curr_list

    def on_registered(self, iface: TMInterface) -> None:
        print(f'Registered to {iface.server_name}')
        
    def on_run_step(self, iface: TMInterface, _time: int):
        if _time >= 0:
            state = iface.get_simulation_state()
            self.curr = np.array([state.input_accelerate,
                                state.input_brake,
                                state.input_left,
                                state.input_right])
            screen = ImageGrab.grab(bbox=(0, 40, 640, 519))
            self.screens_list.append(screen)
            self.states_list.append(state)
            self.time.append(_time)
            self.curr_list.append(self.curr)

def main(client):
    server_name = f'TMInterface{sys.argv[1]}' if len(sys.argv) > 1 else 'TMInterface0'
    print(f'Connecting to {server_name}...')
    run_client(client, server_name)
    return (client)

def fill_df(screen, state, _time, curr):
    if np.array_equal(curr, np.array([True, False, False, False])):
        label = 0
    elif np.array_equal(curr, np.array([False, True, False, False])):
        label = 1
    elif np.array_equal(curr, np.array([False, False, True, False])):
        label = 2
    elif np.array_equal(curr, np.array([False, False, False, True])):
        label = 3
    elif np.array_equal(curr, np.array([True, True, False, False])):
        label = 4
    elif np.array_equal(curr, np.array([True, False, True, False])):
        label = 5
    elif np.array_equal(curr, np.array([True, False, False, True])):
        label = 6
    elif np.array_equal(curr, np.array([False, True, True, False])):
        label = 7
    elif np.array_equal(curr, np.array([False, True, False, True])):
        label = 8
    else:
        label = 9

    screen_path = './img_data/img_A01_{}.jpg'.format(_time)
    screen.save(screen_path)
    screen = np.array(screen)
    left_15_distance = recording.count_pixels(screen, 15, (320, 478), ((10, 15, 30), (50, 55, 70)), -1)
    left_30_distance = recording.count_pixels(screen, 30, (320, 478), ((10, 15, 30), (50, 55, 70)), -1)
    left_45_distance = recording.count_pixels(screen, 45, (320, 478), ((10, 15, 30), (50, 55, 70)), -1)
    left_60_distance = recording.count_pixels(screen, 60, (320, 478), ((10, 15, 30), (50, 55, 70)), -1)
    left_75_distance = recording.count_pixels(screen, 75, (320, 478), ((10, 15, 30), (50, 55, 70)), -1)
    right_75_distance = recording.count_pixels(screen, 75, (320, 478), ((10, 15, 30), (50, 55, 70)), 1)
    right_60_distance = recording.count_pixels(screen, 60, (320, 478), ((10, 15, 30), (50, 55, 70)), 1)
    right_45_distance = recording.count_pixels(screen, 45, (320, 478), ((10, 15, 30), (50, 55, 70)), 1)
    right_30_distance = recording.count_pixels(screen, 30, (320, 478), ((10, 15, 30), (50, 55, 70)), 1)
    right_15_distance = recording.count_pixels(screen, 15, (320, 478), ((10, 15, 30), (50, 55, 70)), 1)
    speed = state.display_speed
    df.loc[len(df.index)] = [screen_path,
                            left_15_distance,
                            left_30_distance,
                            left_45_distance,
                            left_60_distance,
                            left_75_distance,
                            right_15_distance,
                            right_30_distance,
                            right_45_distance,
                            right_60_distance,
                            right_75_distance,
                            speed,
                            label]

if __name__ == "__main__":
    client = MainClient(screens_list, states_list, time, curr_list)
    with concurrent.futures.ProcessPoolExecutor() as exec:
        p = exec.submit(main, client)

    result = p.result()
    for i in range(len(result.screens_list)):
        fill_df(result.screens_list[i],
                result.states_list[i],
                result.time[i],
                result.curr_list[i])
    df.to_csv("A01.csv", index=False)