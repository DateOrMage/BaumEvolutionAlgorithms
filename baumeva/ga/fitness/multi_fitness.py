from typing import List, Union, Callable, Any
from .base_fitness import BaseFitness
from baumeva.ga import BasePenalty
from baumeva.ga.multi_ga_data import MultiGaData


class MultiFitness(BaseFitness):
    """
    Class for calculating fitness values of one population in case of multiobjective optimization with VEGA.
    Inherits from BaseFitness
    attribute: __idx_opt_value: list of indices of optimization values from object functions.
    """
    __idx_opt_value: List[int] = None

    def __init__(self, obj_function: Union[Callable[[any, List[Union[int, float]]], Union[int, float, tuple]], Callable[
                               [List[Union[int, float]]], Union[int, float, tuple]]],
                 obj_value: Union[int, float, List[Union[int, float]]] = None,
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

        super().__init__(obj_function, obj_value, input_data, penalty, conditions)

    def get_fitness_score(self, obj_score: Union[int, float], penalty_value: Union[int, float] = 0) ->\
            Union[int, float]:
        """
        Method for calculating fitness score of individual, will be implemented in child classes.

        :param obj_score: object values of an individual.
        :param penalty_value: fitness values (with respect to optimization values) of an individual.
        :return: fitness scores of the individual.
        """
        pass

    def set_opt_value(self) -> None:
        """
        Method for setting indices of optimization values.
        :return: None.
        """
        self.__idx_opt_value = [i for i in reversed(range(len(self.conditions)))
                                if self.conditions[i] == 'optimize']
        self.conditions = list(filter(lambda a: a != 'optimize', self.conditions))

    def check_task(self) -> None:
        """
        Method for definition type of task: conditional or not.
        :return: None.
        """
        super().check_task()

    def check_input(self, values: List[Union[int, float]]) -> List[Union[int, float]]:
        """
        Checks whether the number of values returned from objective function is correct.
        :param values: values of objective function.
        :return: values.
        """
        return list(values)

    def set_obj_score(self, values: List[Union[int, float]], individ: dict) -> None:
        """
        Gets next objective scores from values of objective function.

        :param values: values of objective function
        :param individ: specimen which gets the objective value.
        :return: None.
        """
        individ['obj_score'] = []
        for idx in self.__idx_opt_value:
            individ['obj_score'].append(values.pop(idx))

    def inferior(self, x: dict, y: dict) -> Union[dict, None]:
        """
        Computes the inferior of 2 individuals

        :param x: dict, first individual data.
        :param y: dict, second individual data.
        :return: dict, containing the inferior of x and y if there is one, None if there are no inferior individuals
        """
        x_score = list(self.obj_function(x['phenotype']))
        y_score = list(self.obj_function(y['phenotype']))

        if x_score == y_score:
            return None

        max_score = x_score.copy()
        for i in range(len(y_score)):
            if max_score[i] < y_score[i]:
                max_score[i] = y_score[i]

        if max_score == x_score:
            return x
        elif max_score == y_score:
            return y
        else:
            return None

    def assign_ranks(self, ga_data: MultiGaData) -> None:
        """
        Assigns a rank to every individual in population equal to 1 + number of individuals dominating it

        :return: None
        """
        for individ in ga_data.population:
            individ['rank'] = 1

        for i in range(len(ga_data.population)):
            for j in range(i+1, len(ga_data.population)):
                inf = self.inferior(ga_data.population[i], ga_data.population[j])
                if inf is not None:
                    inf['rank'] += 1

    def execute(self, ga_data: MultiGaData) -> None:
        """
        Calculate and assign fitness scores to individuals in the population.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        if ga_data.population.is_phenotype:
            ga_data.population.get_phenotype()
        self.assign_ranks(ga_data)

        super().execute(ga_data)