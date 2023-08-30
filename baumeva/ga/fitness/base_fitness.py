from abc import ABC, abstractmethod
from typing import Union, Callable, List, Any
from baumeva.ga.penalties.penalty_methods import PenaltyFunction
from baumeva.ga.ga_data import GaData


class BaseFitness(ABC):
    """
    Abstract class for calculating fitness value of one population.
    """
    def __init__(self,
                 obj_function: Union[Callable[[any, List[Union[int, float]]], Union[int, float]], Callable[
                               [List[Union[int, float]]], Union[int, float]]],
                 obj_value: Union[int, float] = None,
                 input_data: Any = None,
                 penalty: PenaltyFunction = None) -> None:
        """
        Initialize the BaseFitness instance.

        :param obj_function: objective function to be solved, not fitness function! Input argument have to type list.
                             Example:
                                def my_func(x:list):
                                    return x[0]*2 - 1
        :param obj_value: desired objective function value.
        :param input_data: additional information for calculating the value of the objective function.
        :param penalty: subclass of PenaltyFunction(), initialization before initialization class BaumEva(),
                               used for conditional optimization.
                               Example: Dynamic([(my_conditional_func_1, 'inequal'), (my_conditional_func_2, 'equal)]).
                               Default: None.
        :return: None
        """

        self.obj_function = obj_function
        self.obj_value = obj_value
        self.input_data = input_data
        self.penalty = penalty

    def get_penalty_value(self, genotype: List[Union[int, float]], idx_generation:  int) -> Union[int, float]:
        """
        Calculate the penalty value of individual by given genotype and idx_generation.

        :param genotype: the genotype of an individual.
        :param idx_generation: the index of the current generation.
        :return: the calculated penalty value.
        """
        if self.penalty is None:
            return 0
        elif isinstance(self.penalty, PenaltyFunction):
            return self.penalty.calculate(genotype, iter_generation=idx_generation)
        else:
            raise Exception(f'Unexpected penalty_method: {self.penalty}')

    @abstractmethod
    def get_scores(self, genotype: List[Union[int, float]], idx_generation:  int) -> tuple:
        """
        Abstract method for calculating scores of individual.

        :param genotype: the genotype of an individual.
        :param idx_generation: the index of the current generation.
        :return: a tuple containing the objective score and fitness score of the individual.
        """
        pass

    def execute(self, ga_data: GaData) -> None:
        """
        Calculate and assign fitness scores to individuals in the population.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        if ga_data.population.is_phenotype:
            ga_data.population.get_phenotype()
            ga_data.population.swap()

        for individ in ga_data.population:
            if individ['score'] is None:
                individ['obj_score'], individ['score'] = self.get_scores(genotype=individ['genotype'],
                                                                         idx_generation=ga_data.idx_generation)
        if ga_data.population.is_phenotype:
            ga_data.population.swap()
