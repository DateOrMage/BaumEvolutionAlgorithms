from abc import ABC, abstractmethod
from typing import Union
from baumeva.ga import GaData


class BaseMutation(ABC):
    def __init__(self, mutation_lvl: Union[str, float] = 'normal'):
        self.mutation_lvl = mutation_lvl  # 'normal', 'weak', 'strong', float = (0, 1)
        self.rnd_samples = 1000

    @abstractmethod
    def execute(self, ga_data: GaData) -> None:
        pass
