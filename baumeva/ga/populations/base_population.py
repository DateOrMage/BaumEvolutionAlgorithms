from abc import ABC, abstractmethod
from typing import List


class BasePopulation(ABC, list):
    is_sorted: bool = False

    @abstractmethod
    def set_params(self, num_individ: int, gens: tuple, input_population: List[list] = None) -> None:
        pass

    @abstractmethod
    def fill(self) -> None:
        pass

    def sort_by_dict(self, key_dict='score', reverse=False) -> None:
        self.sort(key=lambda d: d[key_dict], reverse=reverse)
        if key_dict == 'score':
            self.is_sorted = True

    def add_dict(self, **data) -> None:
        self.append(data)
