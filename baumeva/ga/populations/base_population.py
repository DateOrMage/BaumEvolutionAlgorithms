from abc import ABC, abstractmethod
from typing import List


class BasePopulation(ABC, list):
    """
    Abstract class for representing a population in a genetic algorithm.
    """
    is_sorted: bool = False
    num_individ: int = None
    gens: tuple = None
    input_population: List[list] = None

    @abstractmethod
    def set_params(self, num_individ: int, gens: tuple, input_population: List[list] = None) -> None:
        """
        Set parameters for initializing the population.

        :param num_individ: the number of individuals in the population.
        :param gens: tuple specifying the range of values for each gene.
        :param input_population: optional input population to be used for initialization.

        :return: None
        """
        pass

    @abstractmethod
    def fill(self) -> None:
        """
        Fill the population with individuals according to the specified parameters.

        :return: None
        """
        pass

    def sort_by_dict(self, key_dict='score', reverse=False) -> None:
        """
        Sort the population based on a specified dictionary key.

        :param key_dict: the key in the individual dictionary used for sorting.
        :param reverse: whether to sort in reverse order.

        :return: None
        """
        self.sort(key=lambda d: d[key_dict], reverse=reverse)
        if key_dict == 'score':
            self.is_sorted = True

    def add_dict(self, **data) -> None:
        """
        Add an individual to the population.

        :param data: dictionary containing data for the individual.

        :return: None
        """
        self.append(data)

    def reset_idx_individ(self) -> None:
        """
        Reset indexes ('idx_individ' attribute) of individuals in the population.

        :return: None
        """
        i = 0
        for individ in self:
            individ['idx_individ'] = i
            i += 1

    @staticmethod
    @abstractmethod
    def get_empty_copy():
        pass
