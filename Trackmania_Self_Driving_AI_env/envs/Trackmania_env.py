import gymnasium as gym
from gymnasium import error, spaces, utils
from gymnasium.utils import seeding
import Script
import recording
import pyautogui
import pydirectinput
import numpy as np
import matplotlib.pyplot as plt
import time

class TrackmaniaEnv(gym.Env):
    def __init__(self, client):
        '''
        This function should define the action space and observation space as well as init the environment
        '''
        self.action_space = spaces.Discrete(8)
        self.observation_space = spaces.Box(low=0, high=255, shape=(479, 640, 3), dtype=np.uint8)
        self.client = client
        if client.iface:
            self.state = self.client.iface.get_simulation_state()
        else:
            while client.iface == None:
                time.sleep(0)
            self.state = self.client.iface.get_simulation_state()

        self.player_info = self.state.player_info
        if self.player_info:
            self.speed = self.player_info.display_speed
            self.rear_gear = self.state.scene_mobil.engine.rear_gear
            self.lateral_contact = self.state.scene_mobil.has_any_lateral_contact
        else:
            self.speed = 0
            self.rear_gear = 0
            self.lateral_contact = False

        self.STEP_LIMIT = 5000
        self.steps = 0
        self.reset()

    def step(self, action):
        '''
        This funtion should define how the agent steps through the environment and return the reward
        from that step as well as the state of the environment and whether the agent is done or not
        '''
        self.take_action(action)
        self.state = self.client.iface.get_simulation_state()
        self.player_info = self.state.player_info
        if self.player_info:
            self.speed = self.player_info.display_speed
        else:
            self.speed = 0
        observation = np.array(recording.ImageGrab.grab(bbox=(0, 40, 640, 519)))
        distance_array = [recording.count_pixels(observation, 15, (320, 478), ((10, 15, 30), (50, 55, 70)), -1),
        recording.count_pixels(observation, 30, (320, 478), ((10, 15, 30), (50, 55, 70)), -1),
        recording.count_pixels(observation, 45, (320, 478), ((10, 15, 30), (50, 55, 70)), -1),
        recording.count_pixels(observation, 60, (320, 478), ((10, 15, 30), (50, 55, 70)), -1),
        recording.count_pixels(observation, 75, (320, 478), ((10, 15, 30), (50, 55, 70)), -1),
        recording.count_pixels(observation,  75, (320, 478), ((10, 15, 30), (50, 55, 70)), 1),
        recording.count_pixels(observation,  60, (320, 478), ((10, 15, 30), (50, 55, 70)),  1),
        recording.count_pixels(observation,  45, (320, 478), ((10, 15, 30), (50, 55, 70)),  1),
        recording.count_pixels(observation,  30, (320, 478), ((10, 15, 30), (50, 55, 70)),  1),
        recording.count_pixels(observation,  15, (320, 478), ((10, 15, 30), (50, 55, 70)),  1)]

        reward = self.calculate_reward(distance_array)
        done = self.game_state()

        info = {"score": reward}
        self.steps += 1
        return observation, reward, done, info
    
    def take_action(self, action):
        if action == 0:
            self.client.iface.set_input_state(accelerate=True)
        elif action == 1:
            self.client.iface.set_input_state(accelerate=False)
        elif action == 2:
            self.client.iface.set_input_state(brake=True)
        elif action == 3:
            self.client.iface.set_input_state(brake=False)
        elif action == 4:
            self.client.iface.set_input_state(left=True)
        elif action == 5:
            self.client.iface.set_input_state(left=False)
        elif action == 6:
            self.client.iface.set_input_state(right=True)
        elif action == 7:
            self.client.iface.set_input_state(right=False)

    def reset(self):
        '''
        This function should reset the environment to its initial state
        '''
        self.steps = 0
        self.client.iface.give_up()
        return recording.np.array(recording.ImageGrab.grab(bbox=(0, 40, 640, 519))) 

    def calculate_reward(self, array):
        reward = 0
        reward += self.speed
        if self.rear_gear:
            reward += -1
        if any(i.real_time_state.has_ground_contact for i in self.state.simulation_wheels):
            reward += -1
        if any(i.real_time_state.contact_material_id != 16 and 
               i.real_time_state.contact_material_id != 9 and
                i.real_time_state.contact_material_id != 6 for i in self.state.simulation_wheels):
            reward += -10
        if any(i <= 30 for i in array) or self.lateral_contact:
            reward += -10000
        return reward
    
    def game_state(self):
        if self.steps >= self.STEP_LIMIT:
            return True
        
        elif self.player_info.race_finished:
            return True
        
        else:
            return False
        
    def render(self, mode='human'):
        
        '''
        This function should define how the environment is displayed
        '''
        if mode == "human":
            recording.screen_record()
    def close(self):
        pass


