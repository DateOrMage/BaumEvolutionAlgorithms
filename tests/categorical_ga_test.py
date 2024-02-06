from baumeva import CategoricalGA
import string

def cat_gens_generator(dim: int) -> list:
    gens_params = []
    for _ in range(dim):
        gens_params.append([i for i in string.ascii_lowercase[:10]])
    return gens_params


def func_uni_value(value_list):
    return len(set(value_list))**2 - 1


categorical_ga = CategoricalGA(num_generations=100,
                               num_individ=300,
                               gens=cat_gens_generator(10),
                               obj_function=func_uni_value,
                               obj_value=0,
                               mutation_lvl=0.1,
                               tournament_size=5,
                               early_stop=None)

ga_data = categorical_ga.optimize()
