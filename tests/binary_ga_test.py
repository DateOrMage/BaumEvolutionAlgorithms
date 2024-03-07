from baumeva import BinaryGA
from baumeva.ga import DynamicPenalty, AdaptivePenalty, StaticPenalty
import math
import numpy as np


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

def func_c01(gens: list) -> tuple:
    np_gens = np.array(gens)

    f = 0
    g = 0
    for idx, gen in enumerate(np_gens):
        g += (gen**2 - 5000*math.cos(0.1*math.pi*gen) - 4000)
        f += np.sum(np_gens[:idx+1])**2

    return f, g


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
                             obj_function=func_c01,# parabola_conditions,
                             obj_value=0,
                             penalty=StaticPenalty(equality_intervals = {1: [(-3, 1),(1, 3),(3, np.inf)], 
                                                                        #  1: [(1, 2),(2, 3),(3, np.inf)]
                                                                         },
                                                    equality_r_coef = {1: [50, 100, 500], 
                                                                    #    1: [5, 10, 50]
                                                                       },
                                                    inequality_intervals = {0: [(-3, 1),(1, 3),(3, np.inf)], 
                                                                            # 1: [(10, 20),(20, 30),(30, np.inf)]
                                                                            },
                                                    inequality_r_coef = {0: [100, 400, 600], 
                                                                        #  1 : [1, 3, 5]
                                                                         }),
                             conditions=['optimize', '<=', ], # '!='
                             mutation_lvl=0.35,
                             early_stop=None)

ga_data = binary_ga.optimize()
ga_data_conditions = bin_ga_conditions.optimize()
