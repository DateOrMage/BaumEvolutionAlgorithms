from abc import ABC, abstractmethod
from typing import List, Union


class BasePenalty(ABC):
    """
    Abstract base class for penalty perform.
    """
    def __init__(self, power: Union[int, float] = 1) -> None:
        """
        Initialization BasePenalty instance.
        """
        self.penalty: float = 0
        self.sum_conditional: float = 0
        self.power = power

    @classmethod
    def name(cls) -> str:
        """
        Method for get the class name.
        :return: str, name of class
        """
        return cls.__name__

    @abstractmethod
    def get_sum_conditional_func(self, conditionals: List[str], values: List[float]) -> None:
        """
        Abstract method for sum of conditional_values

        :param conditionals: values of conditionals. Length of values and conditional must be equals!
        :param values: list of conditionals, example: ['<=', '!=', '<=].
                             Possible to use 2 types of conditional only: '<=', '!=';
        :return: None
        """
        pass

    def execute(self, conditionals: List[str], values: List[float], **kwargs) -> float:
        """
        Method for penalties score perform.
        :param values: values of conditionals. Length of values and conditional must be equals!
        :param conditionals: list of conditionals, example: ['<=', '!=', '<=].
                             Possible to use 2 types of conditional only: '<=', '!=';
        :return: self.penalty.
        """
        if len(conditionals) != len(values):
            raise Exception(f'Numbers of values and conditional must be equals, but given number of conditional:'
                            f' {len(conditionals)} and number of values: {len(values)}')
        self.sum_conditional = 0
        self.get_sum_conditional_func(conditionals, values)
        return self.penalty

