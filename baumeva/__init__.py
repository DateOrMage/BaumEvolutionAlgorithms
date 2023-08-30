# author: Aleksei

# version
__version__ = '0.4.0'

# from .ga import GA
from .ga import Dynamic
from .ga import GaData
from .ga import NewGeneration
from .ga import BasePopulation, CatPopulation, OrderCatPopulation, BinaryPopulation, BinaryGrayPopulation
from .ga import BaseFitness, HyperbolaFitness
from .ga import BaseSelection, TournamentSelection, BalancedSelection, RankedSelection
from .ga import BaseCrossover, OrderCrossover, OnePointCrossover, TwoPointCrossover, UniformCrossover
from .ga import BaseMutation, BaseCombinatoryMutation, InversionMutation, SwapMutation, MovementMutation,\
                ShiftMutation, BinStringMutation
from .combinatory_ga import CombinatoryGA
from .binary_ga import BinaryGA
