from abc import ABC, abstractmethod
from typing import Union, Callable, List, Any
from baumeva.ga import BasePenalty
from baumeva.ga.ga_data import GaData
from warnings import warn


class BaseFitness(ABC):
    """
    Abstract class for calculating fitness value of one population.
    attribute: __is_conditional_opt: conditional optimization task or not.
    attribute: __idx_opt_value: index of optimization value from object function.
    """
    __is_conditional_opt: bool = False
    __idx_opt_value: int = None

    def __init__(self,
                 obj_function: Union[Callable[[any, List[Union[int, float]]], Union[int, float, tuple]], Callable[
                               [List[Union[int, float]]], Union[int, float, tuple]]],
                 obj_value: Union[int, float] = None,
                 input_data: Any = None,
                 penalty: BasePenalty = None,
                 conditions: list = None) -> None:
        """
        Initialize the BaseFitness instance.

        :param obj_function: objective function to be solved, not fitness function! Input argument have to type list.
                             Example:
                                def my_func(x:list):
                                    return x[0]*2 - 1
        :param obj_value: desired objective function value.
        :param input_data: additional information for calculating the value of the objective function.
        :param penalty: subclass of BasePenalty(), initialization before initialization subclass of BaseFitness(),
                               used for conditional optimization. Default: None.
        :param conditions: list of strings (optimizer and conditionals) 3 value can be use: 'optimize', '<=', '!='.
                           Default: None.
                           Example: There is objective function: my_obj_func(x1, x2):
                                                                    return x1**2 + x2**2, 1-x1+x2, x1+x2
                                    my_obj_func returns 3 values, first value to optimize, second value must be <= 0,
                                    third value != 0, so have conditions = ['optimize', '<=', '!=']
                                    dp = DynamicPenalty()
                                    HyperbolaFitness(obj_function=my_func, obj_value=0, penalty=dp,
                                                     conditions=['optimize', '<=', '!='])
        :return: None
        """

        self.obj_function = obj_function
        self.obj_value = obj_value
        self.input_data = input_data
        self.penalty = penalty
        self.conditions = ['optimize'] if conditions is None else conditions
        self.check_task()

    def check_task(self) -> None:
        """
        Method for definition type of task: conditional or not.
        :return: None.
        """
        if self.penalty:
            if isinstance(self.penalty, BasePenalty) is False:
                raise Exception(f'Unexpected penalty_method: {self.penalty}')
            if len(self.conditions) <= 1:
                warn(f'Penalty function does not work with this conditionals: {self.conditions}', UserWarning)
            else:
                self.__is_conditional_opt = True
                self.__idx_opt_value = self.conditions.index('optimize')
                self.conditions.remove('optimize')

    def get_penalty_value(self, values: List[Union[int, float]], idx_generation:  int) -> Union[int, float]:
        """
        Calculate the penalty value of individual by given condition values and idx_generation.

        :param values: values of conditions.
        :param idx_generation: the index of the current generation.
        :return: the calculated penalty value.
        """
        if self.penalty.name() == 'DynamicPenalty':
            return self.penalty.execute(conditionals=self.conditions, values=values, iter_generation=idx_generation)
        else:
            return self.penalty.execute(conditionals=self.conditions, values=values)

    def calc_obj_func(self, genotype: List[Union[int, float]]) -> Union[int, float, list]:
        """
        Method for calculating objective function.

        :param genotype: the genotype of an individual.
        :return: one or more values.
        """
        if self.input_data:
            values = self.obj_function(self.input_data, genotype)
        else:
            values = self.obj_function(genotype)
        if self.__is_conditional_opt:
            try:
                if len(values) != (len(self.conditions)+1):
                    raise Exception(f'Number of returned values from objective function must equal length conditions')
            except TypeError:
                raise Exception(f'For conditional optimization the objective function must return more then 1 value.')
            return list(values)
        else:
            try:
                if len(values) > 1:
                    raise Exception(f'Number of returned values from objective function for non-conditional'
                                    f' optimization must be equal 1')
            except TypeError:
                return values

    @abstractmethod
    def get_fitness_score(self, obj_score: Union[int, float], penalty_value: Union[int, float] = 0) ->\
            Union[int, float]:
        """
        Abstract method for calculating fitness score of individual.

        :param obj_score: object value of an individual.
        :param penalty_value: fitness value of an individual.
        :return: fitness score of the individual.
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
                values = self.calc_obj_func(genotype=individ['genotype'])
                if self.__is_conditional_opt:
                    individ['obj_score'] = values.pop(self.__idx_opt_value)
                    penalty_value = self.get_penalty_value(values=values, idx_generation=ga_data.idx_generation)
                    individ['score'] = self.get_fitness_score(individ['obj_score'], penalty_value)
                else:
                    individ['obj_score'] = values
                    penalty_value = 0
                individ['score'] = self.get_fitness_score(individ['obj_score'], penalty_value)

        if ga_data.population.is_phenotype:
            ga_data.population.swap()
