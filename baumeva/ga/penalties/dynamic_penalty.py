from .base_penalty import BasePenalty
from typing import List, Union


class DynamicPenalty(BasePenalty):
    def __init__(self, delta: float = 1, c: float = 0.5, alpha: float = 2, betta: float = 2):
        """
        Initialization DynamicPenalty instance.
        :param delta, c, alpha, betta: params for dynamic penalty.
        """
        super().__init__(power=betta)
        self.delta = delta
        self.c = c
        self.alpha = alpha

    def get_sum_conditional_func(self, conditionals: List[str], values: List[Union[float, int]]) -> None:

        for i, conditional in enumerate(conditionals):
            if conditional == '!=':
                res = abs(values[i])
            elif conditional == '<=':
                res = max(0, values[i])
            else:
                raise Exception(f'Unexpected sign for conditionals: {conditional}, please use "!=" or "<="')
            self.sum_conditional += res**self.power

    def execute(self, conditionals: List[str], values: List[Union[float, int]], iter_generation: int = 0) -> float:
        """
        Method for penalties score perform.

        :param values: values of conditionals. Length of values and conditional must be equals!
        :param conditionals: list of conditionals, example: ['<=', '!=', '<=].
                             Possible to use 2 types of conditional only: '<=', '!=';
        :param iter_generation: number of generation;
        :return: self.penalty.
        """
        super().execute(conditionals, values)
        self.penalty = self.delta * ((self.c * iter_generation) ** self.alpha) * self.sum_conditional
        return self.penalty
