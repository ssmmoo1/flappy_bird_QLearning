import numpy as np
from random import uniform, randint
import pickle

class Agent:

    def __init__(self, table_shape):
        self.q_table = np.zeros(shape=table_shape)
        self.epsilon = 0.75
        self.learning_rate = 0.1
        self.discount = 0.8

        self.reward = None
        self.state = None
        self.action = None

    def load_agent(self, q_table_path):
        with open(q_table_path, "rb") as file:
            self.q_table = pickle.load(file)

    def save_agent(self, q_table_path):
        with open(q_table_path, "wb") as file:
            pickle.dump(self.q_table, file)


    def take_action(self, state):
        #save state
        self.state = state

        if uniform(0, 1) < self.epsilon:
            # exploit
            print(f"Current Action values for state: {self.q_table[state]}")
            self.action = np.argmax(self.q_table[state])
        else:
            # explore
            self.action = randint(0, len(self.q_table[state])-1) #choose random action

        return self.action

    #should be called after take_action
    def set_reward(self, reward):
        self.reward = reward

    #should be called after taking an action and setting reward
    #game should calculate new state based on the action
    def update_q_table(self, new_state):

        # update Q table
        current_q_val = self.q_table[self.state][self.action]
        new_q_val = current_q_val + self.learning_rate * (self.reward + self.discount * np.max(self.q_table[new_state]) - current_q_val)
        self.q_table[self.state][self.action] = new_q_val

