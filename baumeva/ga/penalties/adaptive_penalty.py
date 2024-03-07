from typing import List, Union
from .base_penalty import BasePenalty


class AdaptivePenalty(BasePenalty):
    def __init__(self, 
                 delta: float = 1, 
                 betta_1: float = 1.1, 
                 betta_2: float = 1.2,
                 betta: float = 2) -> None:
        """
        Initialization StaticPenalty instance.
        :param delta, betta_1, betta_2, betta: params for adaptive penalty.
        """
        super().__init__(power = betta)
        self.delta = delta
        self.betta_1 = betta_1
        self.betta_2 = betta_2
        self.betta = betta

        if self.betta_1 <= 1: 
            raise Exception(f"Unexpected betta_1 value: {self.betta_1}. betta_1 should be greater than 1")
        elif self.betta_2 <= 1: 
            raise Exception(f"Unexpected betta_2 value: {self.betta_2}. betta_2 should be greater than 1")
        elif self.betta_1 == self.betta_2:
            raise Exception(f"betta_1 and betta_2 should not be equal")
        
    def get_sum_conditional_func(self, conditionals: List[str], values: List[float]) -> None:
        super().get_sum_conditional_func(conditionals, values)
        for i, conditional in enumerate(conditionals):
            if conditional == '!=':
                res = abs(values[i])
            elif conditional == '<=':
                res = max(0, values[i])
            else:
                raise Exception(f'Unexpected sign for conditionals: {conditional}, please use "!=" or "<="')
            self.sum_conditional += res ** self.power
    
    def execute(self, conditionals: List[str], values: List[float], best_individ, iter_generation: int = 0, **kwargs)\
            -> float:
        """
        Method for penalties score perform.

        :param values: values of conditionals. Length of values and conditional must be equals!
        :param conditionals: list of conditionals, example: ['<=', '!=', '<=].
                             Possible to use 2 types of conditional only: '<=', '!=';
        :param iter_generation: number of generation;
        :return: self.penalty.
        """
        super().execute(conditionals, values, **kwargs)
        lambda_ = 10
        if iter_generation != 0:
            if best_individ["feasible"]:  # "b_i is the best element at generation, feasible region"
                lambda_ = (1 / self.betta_1) * lambda_
            elif not best_individ["feasible"]:  # "b_i is is is the best element at generation, non feasible region"
                lambda_ = self.betta_2 * lambda_
            else:
                lambda_ = lambda_
        else:
            lambda_ = 0 

        self.penalty = self.delta * lambda_ * self.sum_conditional
        return self.penalty
