# BaumEvA - Bauman Evolution Algorithm

BaumEvA is libraries with implemented genetic algorithm(GA).

## Example usage:
```bash
from baumeva import BinaryGA

# function to be optimized
def func_grivanka(value_list):
    res_sum = 0
    res_mpl = 1
    for i, value in enumerate(value_list):
        res_sum += (value*value) / 4000
        res_mpl *= math.cos(value/math.sqrt(i+1))
    return res_sum - res_mpl + 1

# simple method for use GA
binary_ga = BinaryGA(num_generations=100,
                     num_individ=100,
                     gens=((-16, 16, 0.01), (-16, 16, 0.01)),
                     obj_function=func_grivanka,
                     obj_value=0)
data = binary_ga.optimize()
```