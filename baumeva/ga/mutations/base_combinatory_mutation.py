from abc import abstractmethod
from typing import Union
from random import randint
from .base_mutation import BaseMutation
from baumeva.ga import GaData


class BaseCombinatoryMutation(BaseMutation):
    """
    Abstract class for implementing combinatory mutation operations in a genetic algorithm.
    Inherits from BaseMutation.
    """

    def __init__(self, mutation_lvl: Union[str, float] = 'normal') -> None:
        """
        Initialize the BaseCombinatoryMutation instance.

        :param mutation_lvl: Mutation level, can be string ('weak', 'normal', 'strong') or a float from 0 to 1.
        :return: None
        """
        super().__init__(mutation_lvl=mutation_lvl)
        self.mutation_map: dict = {'weak': 0.03, 'normal': 0.1, 'strong': 0.3}
        self.check_mutation()

    def check_mutation(self) -> None:
        """
        Check the validity of the mutation level parameter.

        :return: None
        """
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
        """
        Determine if mutation should be performed.

        :return: True if mutation should be performed, False otherwise.
        """
        if randint(0, self.rnd_samples-1) <= self.mutation_lvl * self.rnd_samples:
            return True
        else:
            return False

    @abstractmethod
    def get_mutation(self, child: dict) -> dict:
        """
        Abstract method for implementation mutation operation.

        :param child: a dictionary representing the child individual.
        :return: the mutated child individual.
        """
        pass

    def execute(self, ga_data: GaData) -> None:
        """
        Execute the mutation operation.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        for child in ga_data.children:
            is_mutation = self.determines_mutation()
            if is_mutation:
                self.get_mutation(child)
