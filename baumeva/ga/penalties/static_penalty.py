from typing import List, Union, Dict 
from .base_penalty import BasePenalty

class StaticPenalty(BasePenalty):
    def __init__(self, 
                 equality_intervals: Dict[int, List[tuple]],
                 equality_r_coef: Dict[int, List[float]],
                 inequality_intervals: Dict[int, List[tuple]],
                 inequality_r_coef: Dict[int, List[float]], ) -> None:
        """
        Initialization StaticPenalty instance.
        :param equality_intervals, equality_r_coef, inequality_intervals, inequality_r_coef: params for static penalty.
        
        Example: There is objective function: x1**2 + x2**2 and 
                            inequality conditionals: 1-x1+x2 <= 0, 
                            equality conditionals: x1+x2 = 0, 
                Therefore our parameters will look like this:
                equality_intervals = {1: [
                                            (0.001, 0.01),
                                            (0.01, 0.1),
                                            (0.1, np.inf)]},
                equality_r_coef = {1: [50, 100, 500]},
                inequality_intervals = {0: [
                                            (100, 300),
                                            (300, 610),
                                            (610, np.inf)]},
                inequality_r_coef = {0: [100, 400, 600]}
                where dictionary keys map to functions accordingly
        """
        super().__init__(power=2)
        self.equality_intervals = equality_intervals
        self.equality_r_coef = equality_r_coef
        self.inequality_intervals = inequality_intervals
        self.inequality_r_coef = inequality_r_coef

        if len(self.equality_r_coef) != len(self.equality_intervals):
            raise Exception("Coefficients length and intervals length are not equal for an equality conditions")
        if len(self.inequality_r_coef) != len(self.inequality_intervals):
            raise Exception("Coefficients length and intervals length are not equal for an inequality conditions")
        
    def get_sum_conditional_func(self, conditionals: List[str], values: List[float]) -> None:

        for i, conditional in enumerate(conditionals):
            # print(conditional)
            if conditional == '!=':
                print(f"i: {i} if conditional == '!=")
                if values[i] != 0:
                    print("if conditional == '!=' values[i] != 0 and res = 0")
                    res = 0
                    continue
                for idx, val in enumerate(self.equality_intervals[i]):
                    print(f"equality_intervals idx {idx} val[0] {val[0]} val[1] : {val[1]}| i: {i}")
                    if values[i] > val[0] and values[i] < val[1]:
                        print(f"self.equality_r_coef[i][idx] * abs(values[i]) : {self.equality_r_coef[i][idx] * abs(values[i])}")
                        res = self.equality_r_coef[i][idx] * abs(values[i])
                    else: 
                        raise Exception(f"Unexpected equality intervals: {self.equality_intervals[i]}")
            elif conditional == '<=':
                print(f"i: {i} conditional == '<='")
                if values[i] <= 0:
                    print(f"i: {i} values[i] <= 0 and res = 0")
                    res = 0
                    continue
                for idx, val in enumerate(self.inequality_intervals[i]):
                    if values[i] > val[0] and values[i] < val[1]:
                        res = self.equality_r_coef[i][idx] * max(0, values[i])
                    else:
                        raise Exception(f"Unexpected inequality intervals: {self.inequality_intervals[i]}")
            else:
                raise Exception(f'Unexpected sign for conditionals: {conditional}, please use "!=" or "<="')
            self.sum_conditional += res ** self.power

    def execute(self, conditionals: List[str], values: List[float], **kwargs) -> float:
        """
        Method for penalties score perform.

        :param values: values of conditionals. Length of values and conditional must be equals!
        :param conditionals: list of conditionals, example: ['<=', '!=', '<='].
                             Possible to use 2 types of conditional only: '<=', '!=';
        :return: self.penalty.
        """
        super().execute(conditionals, values, **kwargs)

        self.penalty = self.sum_conditional
        return self.penalty