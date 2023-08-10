from abc import ABC, abstractmethod
from typing import List


class BasePopulation(ABC, list):
    is_sorted: bool = False
    num_individ: int = None
    gens: tuple = None
    input_population: List[list] = None

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

    def add_idx_individ(self) -> None:
        i = 0
        for individ in self:
            individ['idx_individ'] = i
            i += 1
