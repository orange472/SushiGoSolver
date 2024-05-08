from abc import ABC, abstractmethod
from state import SushiGoState
from typing import List


class Agent(ABC):
    @abstractmethod
    def select_action(self, state: SushiGoState) -> List[int]:
        pass
