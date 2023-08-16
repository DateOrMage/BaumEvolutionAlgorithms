from abc import ABC, abstractmethod
from typing import Union
from baumeva.ga import GaData


class BaseMutation(ABC):
    """
    Abstract class for implementing mutation operations in a genetic algorithm.
    """

    def __init__(self, mutation_lvl: Union[str, float] = 'normal'):
        """
        Initialize the BaseMutation instance.

        :param mutation_lvl: Mutation level, can be string ('weak', 'normal', 'strong') or a float from 0 to 1.
        :return: None
        """
        self.mutation_lvl = mutation_lvl  # 'normal', 'weak', 'strong', float = (0, 1)
        self.rnd_samples = 1000

    @abstractmethod
    def execute(self, ga_data: GaData) -> None:
        """
        Execute the mutation operation.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        pass
