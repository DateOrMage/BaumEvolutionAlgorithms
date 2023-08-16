from abc import abstractmethod
from typing import Union
from random import randint
from .base_mutation import BaseMutation
from baumeva.ga import GaData


class BaseCombinatoryMutation(BaseMutation):
    def __init__(self, mutation_lvl: Union[str, float] = 'normal') -> None:
        super().__init__(mutation_lvl=mutation_lvl)
        self.mutation_map: dict = {'weak': 0.03, 'normal': 0.1, 'strong': 0.3}
        self.check_mutation()

    def check_mutation(self) -> None:
        if type(self.mutation_lvl) is str:
            if self.mutation_lvl in self.mutation_map.keys():
                self.mutation_lvl = self.mutation_map[self.mutation_lvl]
            else:
                raise Exception(f'{self.mutation_lvl} is not expected, please use one of this:'
                                f' ("normal", "weak", "strong") or float value from 0 to 1')
        elif type(self.mutation_lvl) is float:
            if self.mutation_lvl < 0 or self.mutation_lvl > 1:
                raise Exception(f'{self.mutation_lvl} is not expected, please use one of this:'
                                f' ("normal", "weak", "strong") or float value from 0 to 1')
        else:
            raise Exception(f'{self.mutation_lvl} is not expected, please use one of this:'
                            f' ("normal", "weak", "strong") or float value from 0 to 1')

    def determines_mutation(self) -> bool:
        if randint(0, self.rnd_samples-1) <= self.mutation_lvl * self.rnd_samples:
            return True
        else:
            return False

    @abstractmethod
    def get_mutation(self, child):
        pass

    def execute(self, ga_data: GaData) -> None:
        for child in ga_data.children:
            is_mutation = self.determines_mutation()
            if is_mutation:
                self.get_mutation(child)
