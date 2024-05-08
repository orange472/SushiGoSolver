from state import SushiGoState
from agent import Agent
import random


class RandomAgent(Agent):
    def __init__(self):
        pass

    def select_action(self, state: SushiGoState):
        return [random.choice(state.cur_hand)]
