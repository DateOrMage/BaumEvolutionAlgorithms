from typing import Union, Callable, Optional, List, Tuple
from support_funcs.support_functions import get_sum_conditional_func


class PenaltyFunction:
    """
    Class for creation and calculation penalty for conditional optimization.
    """
    def __init__(self, conditional_func: List[Tuple[Callable[[List[Union[int, float]]], Union[int, float]], str]],
                 penalty: Union[int, float] = 0) -> None:
        """
        :param conditional_func: list[tuple[Callable[[list[Union[int, float]]], Union[int, float]], str]] - conditional
                                 function. Used only 2 types of conditional: g(x) <= 0 ('inequal') or
                                 h(x) == 0 ('equal'). Example: def my_f1(x: list[int|float]) -> int|float:
                                 return sum(x) - 1; def my_f2(x: list[int|float]) -> int|float: return max(x);
                                 conditional_func = [(my_f1, 'equal'), (my_f2, 'inequal')]
        :param penalty: int or float, default: 0.
        """
        if conditional_func is None:
            raise Exception(f'conditional_func cannot be NoneType object'
                            f' if used conditional optimization, have to use {List[Tuple]}')
        elif type(conditional_func) != list:
            raise Exception(f'Type of conditional_func must be list, not {type(conditional_func)}')
        elif len(conditional_func) == 0:
            raise Exception(f'conditional_func cannot be empty')
        else:
            for tpl in conditional_func:
                if type(tpl) != tuple:
                    raise Exception(f'Type of elements conditional_func must be tuple, not {type(tpl)}')
                elif len(tpl) != 2:
                    raise Exception(f'Incorrect size of tuple, excepted - 2, given - {len(tpl)}')
                elif (tpl[1] != 'equal') and (tpl[1] != 'inequal'):
                    raise Exception(f'Unexpected value: {tpl[1]}, must be "equal" or "inequal"')
                else:
                    self.conditional_func = conditional_func
        self.penalty = penalty

    def calculate(self, gens: list, iter_generation: Optional[int]) -> Union[int, float]:
        return self.penalty


class Dynamic(PenaltyFunction):

    def __init__(self, conditional_func, delta: float = 1, c: float = 0.5, alpha: float = 2, betta: float = 2):
        super().__init__(conditional_func)
        self.delta = delta
        self.c = c
        self.alpha = alpha
        self.betta = betta

    @classmethod
    def name(cls):
        return cls.__name__

    def calculate(self, gens, iter_generation):
        super().calculate(gens, iter_generation)
        sum_func = get_sum_conditional_func(self.conditional_func, gens=gens, power=self.betta)
        self.penalty = self.delta*((self.c*iter_generation)**self.alpha)*sum_func
        return self.penalty


if __name__ == '__main__':
    def my_func(gen_list):
        res = 0
        for gen in gen_list:
            res += gen
        return res

    # pen_method = Dynamic([(my_func, 'das')])

    # pen_method = Dynamic([(my_func, 'equal'), (my_func, 'inequal')])
    # pen = pen_method.calculate([1, 2, 3], 2)
    # print(pen)

    # pen_method = PenaltyFunction([(my_func, 'equal'), (my_func, 'inequal')])
    # pen = pen_method.calculate([1, 2, 3], 1)
    # print(pen)
