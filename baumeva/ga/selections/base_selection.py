from abc import ABC, abstractmethod
from baumeva.ga import GaData


class BaseSelection(ABC):
    """
    Abstract class for implementing selection operations in a genetic algorithm.
    """

    def execute(self, ga_data: GaData) -> None:
        """
        Execute the selection operation.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        ga_data.population.reset_idx_individ()
        ga_data.parents = ga_data.population.get_empty_copy()
