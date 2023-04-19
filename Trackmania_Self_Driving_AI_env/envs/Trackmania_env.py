import gym
from gym import error, spaces, utils
from gym.utils import seeding

class Trackmania_env(gym.Env):
    def __init__(self):
        '''
        This function should define the action space and observation space as well as init the environment
        '''
        self.action_space = spaces.Discrete(4)
        self.reset()

    def step(self, action):
        '''
        This funtion should define how the agent steps through the environment and return the reward
        from that step as well as the state of the environment and whether the agent is done or not
        '''
        return observation, reward, done, info

    def reset(self):
        '''
        This function should reset the environment to its initial state
        '''

    def render(self, mode='human'):
        '''
        This function should define how the environment is displayed
        '''

    def close(self):
        pass