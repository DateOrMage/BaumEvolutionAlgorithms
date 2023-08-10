from abc import ABC, abstractmethod
from typing import Union, Callable, List, Any
from baumeva.ga.penalties.penalty_methods import PenaltyFunction
from baumeva.ga.ga_data import GaData


class BaseFitness(ABC):
    def __init__(self,
                 obj_function: Union[Callable[[any, List[Union[int, float]]], Union[int, float]], Callable[
                               [List[Union[int, float]]], Union[int, float]]],
                 obj_value: Union[int, float] = None,
                 input_data: Any = None,
                 penalty: PenaltyFunction = None) -> None:

        self.obj_function = obj_function
        self.obj_value = obj_value
        self.input_data = input_data
        self.penalty = penalty

    def get_penalty_value(self, genotype: List[Union[int, float]], idx_generation:  int) -> Union[int, float]:
        if self.penalty is None:
            return 0
        elif isinstance(self.penalty, PenaltyFunction):
            return self.penalty.calculate(genotype, iter_generation=idx_generation)
        else:
            raise Exception(f'Unexpected penalty_method: {self.penalty}')

    @abstractmethod
    def get_scores(self, genotype: List[Union[int, float]], idx_generation:  int) -> tuple:
        pass

    def execute(self, data: GaData) -> None:
        for individ in data.population:
            individ['obj_score'], individ['score'] = self.get_scores(genotype=individ['genotype'],
                                                                     idx_generation=data.idx_generation)

