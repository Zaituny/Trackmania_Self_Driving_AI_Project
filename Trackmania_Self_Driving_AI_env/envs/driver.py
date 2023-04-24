import Script
import Trackmania_env
import time

client = Script.MainClient()
Script.threading.Thread(target=Script.main, daemon=False, args=[client]).start()

env = Trackmania_env.TrackmaniaEnv(client)

time.sleep(1)

from PIL import Image  # To transform the image in the Processor
import numpy as np
import gymnasium as gym

# Convolutional Backbone Network
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Convolution2D, Permute
from keras.optimizers import Adam
# Keras-RL
from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory
from rl.core import Processor
from rl.callbacks import FileLogger, ModelIntervalCheckpoint

nb_actions = env.action_space.n

IMG_SHAPE = (84, 112)
WINDOW_LENGTH = 1

class ImageProcessor(Processor):
    def process_observation(self, observation):
        # First convert the numpy array to a PIL Image
        img = Image.fromarray(observation)
        # Then resize the image
        img = img.resize(IMG_SHAPE)
        # And convert it to grayscale  (The L stands for luminance)
        img = img.convert("L")
        # Convert the image back to a numpy array and finally return the image
        img = np.array(img)
        return img.astype('uint8')  # saves storage in experience memory
    
    def process_state_batch(self, batch):

        # We divide the observations by 255 to compress it into the intervall [0, 1].
        # This supports the training of the network
        # We perform this operation here to save memory.
        processed_batch = batch.astype('float32') / 255.
        return processed_batch

    def process_reward(self, reward):
        return reward
    
input_shape = (WINDOW_LENGTH, IMG_SHAPE[1], IMG_SHAPE[0])

model = Sequential()
model.add(Permute((2, 3, 1), input_shape=input_shape))

model.add(Convolution2D(32, (8, 8), strides=2, kernel_initializer='he_normal'))
model.add(Activation('relu'))
model.add(Convolution2D(64, (4, 4), strides=2,kernel_initializer='he_normal'))
model.add(Activation('relu'))
model.add(Convolution2D(64, (3, 3), kernel_initializer='he_normal'))
model.add(Activation('relu'))
model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))

memory = SequentialMemory(limit=1000000, window_length=WINDOW_LENGTH)

processor = ImageProcessor()

policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.1, value_test=.05,
                              nb_steps=1000000)

dqn = DQNAgent(model=model, nb_actions=nb_actions, policy=policy, memory=memory,
               processor=processor, nb_steps_warmup=50000, gamma=.99, target_model_update=1000,
              train_interval=4, delta_clip=1)

dqn.compile(Adam(learning_rate=.00025), metrics=['mae'])

weights_filename = 'test_dqn_mania_weights.h5f'
checkpoint_weights_filename = './experiment_3_weights/test_dqn_' + "mania" + '_weights_{step}.h5f'
checkpoint_callback = ModelIntervalCheckpoint(checkpoint_weights_filename, interval=10000)

dqn.fit(env, nb_steps=1000000, callbacks=[checkpoint_callback], log_interval=100000, visualize=False)

# After training is done, we save the final weights one more time.
dqn.save_weights(weights_filename, overwrite=True)