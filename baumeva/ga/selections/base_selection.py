from abc import ABC
from typing import Optional
from baumeva.ga import GaData
from baumeva.global_generator import generator


class BaseSelection(ABC):
    """
    Abstract class for implementing selection operations in a genetic algorithm.
    """
    rnd_seed: Optional[int] = None

    def __init__(self) -> None:
        #super().__init__()
        self.rnd_seed = generator.rnd_seed

    def execute(self, ga_data: GaData) -> None:
        """
        Execute the selection operation.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        ga_data.population.reset_idx_individ()
        ga_data.parents = ga_data.population.get_empty_copy()
