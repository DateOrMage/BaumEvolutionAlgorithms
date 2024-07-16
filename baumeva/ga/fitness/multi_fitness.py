from .base_fitness import BaseFitness
from typing import List, Union


class MultiFitness(BaseFitness):
    """
    Class for calculating fitness values of one population in case of multiobjective optimization with VEGA.
    Inherits from BaseFitness
    attribute: __idx_opt_value: list of indices of optimization values from object functions.
    """
    __idx_opt_value: List[int] = None

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
