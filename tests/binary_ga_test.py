from baumeva import BinaryGA
from baumeva.ga import DynamicPenalty
import math


def func_grivanka(value_list):
    res_sum = 0
    res_mpl = 1
    for i, value in enumerate(value_list):
        res_sum += (value*value) / 4000
        res_mpl *= math.cos(value/math.sqrt(i+1))
    return res_sum - res_mpl + 1


def parabola_conditions(x: list) -> tuple:
    res = -x[0]*x[0] + 9
    condition_1 = -x[0]-3
    condition_2 = x[0]+3
    return res, condition_1, condition_2


binary_ga = BinaryGA(num_generations=100,
                     num_individ=100,
                     gens=((-16, 16, 0.01), (-16, 16, 0.01)),
                     obj_function=func_grivanka,
                     obj_value=0,
                     is_gray=True,
                     mutation_lvl=0.35,
                     early_stop=None)

bin_ga_conditions = BinaryGA(num_generations=100,
                             num_individ=100,
                             gens=((-5, 5, 0.001),),
                             obj_function=parabola_conditions,
                             obj_value=0,
                             penalty=DynamicPenalty(),
                             conditions=['optimize', '<=', '!='],
                             mutation_lvl=0.35,
                             early_stop=None)

ga_data = binary_ga.optimize()
ga_data_conditions = bin_ga_conditions.optimize()
