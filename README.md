<div align="center">
  <img src="https://raw.githubusercontent.com/DateOrMage/BaumEvolutionAlgorithms/f3b6ec56ff5fd8271ba37f293de2df3337ba27bd/logo.svg">
</div>

# BaumEvA - Bauman Evolution Algorithm

BaumEvA is an advanced genetic algorithm crafted in Python. It's designed to work with both binary and combinatorial data types, providing a comprehensive suite of tools for optimization and search tasks. Baumeva offers a variety of selection, crossover, mutation, and parent selection mechanisms.

## Installation

To install the BaumEvA, run the following command:

```bash
pip install baumeva
```

## Usage

### Quickstart

You can start with class `BinaryGA` which already equipped with predefined methods: tournament selection, one-point crossover and simple mutation. This class alows users to engage with binary genetic algorithm effortlessly. 

```python
from baumeva import BinaryGA
import math

def func_grivanka(value_list):
    res_sum = 0
    res_mpl = 1
    for i, value in enumerate(value_list):
        res_sum += (value*value) / 4000
        res_mpl *= math.cos(value/math.sqrt(i+1))
    return res_sum - res_mpl + 1
```

This simple function is used to evaluate the solution. In this case we are looking for the minimum of the grivank function.

```python
# simple method for use GA
binary_ga = BinaryGA(num_generations=100,
                     num_individ=100,
                     gens=((-16, 16, 0.01), (-16, 16, 0.01)),
                     obj_function=func_grivanka,
                     obj_value=0,
                     is_gray=True,
                     mutation_lvl=0.35,
                     early_stop=None)
ga_data = binary_ga.optimize()
```

The `num_generations` specifies the total number of generations.

The `num_individ` specifies the total number of individuals in a population. 

The `gens` specifies the range and precision for each gene in the binary representation. Tuple contains minimum value for the gene, maximum value for the gene, precision for the gene's value (the step). 
In the example given gens=((-16, 16, 0.01), (-16, 16, 0.01)) signifies two genes, both ranging from -16 to 16 with a step of 0.01. `BinaryGA` works not with real numbers but with binary representation. 

The `obj_function` specifies the objective function that evaluates the object score of each individual. 

The `obj_value` defines the target or optimal value the algorithm aims to achieve or get as close as possible to.

The `is_gray` uses gray code to convert to binary representation, default: False.

The `mutation_lvl` is probability of mutation of each bit; float or string value, default: 'normal' meaning a probability equal to 1/s, where s is the length of the binary string.

The `early_stop` determines the number of generations N. If the best individual is not updated within N generations in a row, then the algorithm stops; int or None, default: 10.

You can get the best solution calling `ga_data.best_solution`.

There are also special class for combinatory genetic algorithm - `CombinatoryGA`. The only difference is `gens` parameter. For example: (0, 9, 10), 0 - first categorical value,
                     9 - last categorical value, step between categorical is 1 (const), 10 - number of categorical
                     values in every individ.

#### Categorical Genetic Algorithm example usage

For optimization in categorical parameter space you should utilize `CategoricalGA`. Example of `CategoricalGA` usage described below.

```python
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
                               tournament_size=10,
                               early_stop=None)

ga_data = categorical_ga.optimize()
```

Constructor of `CategoricalGA` have the same set of arguments as `BinaryGA` except of `is_gray`.
Note that if you want to create some or all genes as list of values you should use `list`, not `tuple`. For example `["a", "b", "c", "d"]` should be list. If you'd like to use standard range of values to define gene use `tuple`, for example `(1, 10, 1)` for numbers from 1 to 10.

#### Conditional optimization

For conditional optimization tasks you can use same classes `BinaryGA`, `CombinatoryGA`, `CategoricalGA`  with two additional parameters: `penalty`, `conditions`.

The `penalty` is penalty function, subclass of `BasePenalty()`, initialization before
                        initialization subclass of `BaseFitness()`, used for conditional optimization.

The `conditions` is list of conditionals, 3 value can be use: 'optimize', '<=', '!='

Example conditional optimization task:
```python
from baumeva import BinaryGA
from baumeva.ga import DynamicPenalty

def parabola_conditions(x: list) -> tuple:
    res = -x[0]*x[0] + 9
    condition_1 = -x[0]-3
    condition_2 = x[0]+3
    return res, condition_1, condition_2

bin_ga_conditions = BinaryGA(num_generations=100,
                             num_individ=100,
                             gens=((-5, 5, 0.001),),
                             obj_function=parabola_conditions,
                             obj_value=0,
                             penalty=DynamicPenalty(),
                             conditions=['optimize', '<=', '!='],
                             is_gray=True,
                             mutation_lvl=0.35,
                             early_stop=None)

ga_data_conditions = bin_ga_conditions.optimize()
```
There is object function `parabola_conditions`, which return 3 values. The `res` is value for optimization, the `condition_1` is value less or equal 0, the `condition_2` is value not equal 0. So we have `conditions=['optimize', '<=', '!=']` and use `DynamicPenalty()`.

### Advanced Usage

Additionally, BaumEva offers a modular approach for those who desire more customization. By directly declaring specific classes, you can handpick from a wide range of mutation, selection and crossover methods, crafting a customized genetic algorithm.

```python
from random import shuffle
from baumeva.ga import GaData, OrderCatPopulation, HyperbolaFitness, TournamentSelection, OrderCrossover, SwapMutation, NewGeneration

def func_word(word: list) -> float:
    obj_word = 'ALGORITHM'
    res = 0
    for idx, litter in enumerate(word):
        if litter != obj_word[idx]:
            res += 1
    return res

input_population_size = 100
input_word = list("ALGORITHM")
in_pop = []
for i in range(input_population_size):
    shuffle(input_word)
    in_pop.append(input_word.copy())


def print_result(data: dict) -> None:
    print("Best result: ")
    for key in data.keys():
        print(f"{key}: {data[key]}")

ga_data = GaData(num_generations=100, early_stop=60)
ocp = OrderCatPopulation()
ocp.set_params(num_individ=input_population_size, gens=(0, 8, 9), input_population=in_pop)
ocp.fill()
ga_data.population = ocp
fitness_func = HyperbolaFitness(obj_function=func_word, obj_value=0)
fitness_func.execute(ga_data)
ga_data.update()

selection = TournamentSelection(tournament_size=6)
crossover = OrderCrossover()
mutation = SwapMutation(0.35)
new_generation = NewGeneration('best')

for i in range(ga_data.num_generations):

  selection.execute(ga_data)
  crossover.execute(ga_data)
  mutation.execute(ga_data)
  new_generation.execute(ga_data)
  fitness_func.execute(ga_data)
  ga_data.update()

  if ga_data.num_generation_no_improve >= ga_data.early_stop:
      print(f'Early stopping: {i} generation')
      break
  if ga_data.best_solution['obj_score'] == 0:
      print(f'Goal achieved: {i} generation')
      break

print(f"Result: {ga_data.best_solution} ")
```

This example demonstrates the use of the BaumEvA library to search for the word "ALGORITHM" using a combination genetic algorithm.

### Collector Usage

Another way of use of the library is the "collector mode", which allows to collect a customized GA, just like the "advanced mode", but at the same time it is much easier to use.

```python
from baumeva import CollectorGA
from baumeva.ga import BinaryPopulation, HyperbolaFitness, TournamentSelection, OnePointCrossover,\
    BinStringMutation, NewGeneration


def generate_gens_params(one_gen: list, num_gens: int) -> list:
    gens_params = []
    for _ in range(num_gens):
        gens_params.append(one_gen)
    return gens_params


def one_max(gens: list) -> float:
    return sum(gens) / len(gens)


my_ga = CollectorGA(fitness=HyperbolaFitness(obj_function=one_max, obj_value=1),
                    selection=TournamentSelection(5),
                    crossover=OnePointCrossover(),
                    mutation=BinStringMutation(0.15),
                    new_generation=NewGeneration('best'))

my_ga.set_population(population=BinaryPopulation,
                     num_individ=100,
                     num_generations=100,
                     gens=generate_gens_params([0, 1, 1], 30),
                     early_stop=35)

my_ga.optimize()
```

This example demonstrates the optimization of function one_max() using elements of binary genetic algorithm.


### Components Used:

1. **GaData**: Class for holding and managing data related to a genetic algorithm run.
2. **OrderCatPopulation**: Class for representing ordered categorical population in a genetic algorithm. In this case we set the first population manually using `in_pop` - a list consisting of words anagrams to 'ALGORITHM'.
3. **HyperbolaFitness**: Class for calculating fitness value using the hyperbola approach. Object function is levenstein distance between the evolved string and the target string 'ALGORITHM'.
4. **TournamentSelection**: Selection method used, which operates on tournament-based selection logic.
5. **OrderCrossover**: The crossover mechanism used in the genetic algorithm.
6. **InversionMutation**: Mutation method, introducing randomness in the population.
7. **NewGeneration**: Utility for generating new population members based on chosen criteria.

### How it works:

1. The genetic algorithm data parameters are initialized, and the initial population is set and filled.
2. The fitness of each individual in the population is calculated based on it`s distance from the target word 'ALGORITHM'.
3. In each generation:
    - The tournament-based selection method is applied.
    - Pairs of individuals undergo crossover using the order-based crossover mechanism.
    - Mutation is applied to individuals with some probability.
    - A new generation is created based on the best individuals.
    - Fitness is recalculated for the new generation.
4. The genetic algorithm either runs for a predefined number of generations or stops early if there hasn't been an improvement in the population fitness for a specified number of generations.
5. The result is the closest approximation found to the word 'algorithm'.

### Multi-Objective optimization

BaumEvA supports multi-objective optimization using the VEGA and FFGA algorithms. 

The simplest way to run them is by using the VEGA and FFGA classes:

```python
def quadratic(x: list) -> tuple:
    return (x[0] - 2)**2 + (x[1] - 2)**2, x[0]*x[0] + x[1]*x[1], (x[0] - 4)**2 + (x[1] - 1)**2

vega = VEGA(num_generations=100,
            num_individ=100,
            gens=((0, 100, 0.01),)*2,
            obj_function=quadratic,
            is_gray=False,
            mutation_lvl=0.05,
            early_stop=None)

ga_data = vega.optimize()
```

#### Advanced usage

Modular approach is applicable to multi-objective optimization as well:

```python
from baumeva.ga import MultiGaData, BinaryPopulation, FFGAFitness, TournamentSelection, OnePointCrossover, \
                       BinStringMutation, MultiNewGeneration, DynamicPenalty

def rcm03(x: list) -> tuple:
    f1 = x[0]*(16+x[2]**2)**0.5 + x[1]*(1+x[2]**2)**0.5
    f2 = 20*(16+x[2]**2)**0.5 / (x[2]*x[0])
    g1 = f1 - 0.1
    g2 = f2 - 10000
    g3 = 80*(1+x[2]**2)**0.5 / (x[2]*x[1]) - 10000
    return f1, f2, g1, g2, g3

ga_data = MultiGaData(num_generations=100, early_stop=20)        

population = BinaryPopulation()
population.set_params(num_individ=100, gens=((0.00001, 100, 0.01), (0.00001, 100, 0.01), (1, 3, 0.01)))
population.fill()

ga_data.population = population
fitness_func = FFGAFitness(obj_function=rcm03, conditions=['optimize']*2 + ['<=']*3, penalty=DynamicPenalty())
fitness_func.execute(ga_data)
ga_data.update()

selection = TournamentSelection(tournament_size=6)
crossover = OnePointCrossover()
mutation = BinStringMutation(0.15)
new_generation = MultiNewGeneration('best')

for i in range(ga_data.num_generations):

  selection.execute(ga_data)
  crossover.execute(ga_data)
  mutation.execute(ga_data)
  new_generation.execute(ga_data)
  fitness_func.execute(ga_data)
  ga_data.update()

  if ga_data.num_generation_no_improve >= ga_data.early_stop:
      print(f'Early stopping: {i} generation')
      break


print(f"Result:")
ga_data.print_best_solution()
```

Note that we use MultiGaData class instead of GaData for storing the algorithm data during its run.

#### Collector Usage

Classes for multi-objective optimization also support the collector mode:

```python
from baumeva import CollectorGA
from baumeva.ga import BinaryPopulation, VEGAHyperbolaFitness, VEGABalancedSelection, OnePointCrossover,\
    BinStringMutation, NewGeneration, DynamicPenalty, MultiGaData

def multilinear_conditions(x: list) -> tuple:
    return -4*x[0]-2*x[1], -2*x[0]-4*x[1], -3*x[0]-9*x[1], -8*x[0]-2*x[1], -4*x[0]+x[1], -3*x[0]+2*x[1], 2*x[0] - 4*x[1], \
        3*x[0] - x[1], 4*x[0] + 3*x[1], 2*x[0]+3*x[1], -x[0]+3*x[1], 2*x[0]-x[1], -x[0], -x[1]

moga = CollectorGA(fitness=VEGAHyperbolaFitness(obj_function=multilinear_conditions, obj_value=[0,]*9,
                                                conditions=['optimize']*9 + ['<=']*5, penalty=DynamicPenalty()),
                   selection=VEGABalancedSelection(9),
                   crossover=OnePointCrossover(),
                   mutation=BinStringMutation(0.05),
                   new_generation=NewGeneration('best'),
                   storage=MultiGaData)

moga.set_population(population=BinaryPopulation,
                    num_individ=100,
                    num_generations=1000,
                    gens=((0, 100, 0.01), (0, 100, 0.01)))

moga.optimize()
```

## Documentation

Still in progress. For now, you can read brief description of the library classes.

### BinaryGA
Class for perform binary genetic algorithm. 
Supports the following parameters:
- `num_generations (int)` - number of generations;
- `num_individ (int)` - number of individuals in generation (size of population);
- `gens (tuple)` - controls the gens type;
- `obj_function (Callable)` - object function with 1 or 2 arguments, my_func(gens: list) or
                             my_func(input_data: Any, gens: list);
- `obj_value (int | float, default: None)` - if object value exists, GA will optimize to the value,
                          else GA will optimize to min;
- `input_data (Any, default: None)` - argument for object function, you can pass any additional information to object function;
- `penalty (class PenaltyFunction, default: None)` - subclass of PenaltyFunction(), used for conditional optimization;
- `conditions (list of strings (optimizer and conditionals), default: None.)` -  3 value can be use: 'optimize', '<=', '!=';
- `is_gray (bool, default: False)` - ability to use gray code instead of binary representation;
- `children_percent (float, default: 0.95)` - percent of children in new generation;
- `early_stop (int, default: 10)` - early stopping criteria, number of generation without improve;
- `input_population (list[list], default: None)` - first generation from user to improve ga work;
- `tournament_size (int, default: 3)` - size of tournament in selection;
- `mutation_lvl (str | float, default: 'normal')` - mutation probability, can accept float value or string: 'weak', 'normal', 'strong';
- `transfer_parents (str, default: "best")` - type of transfer parents: "best" or "random".

### CombinatoryGA and CategoricalGA
Class for perform combinatory genetic algorithm (categorical order combinations without repetitions). 
Supports all above parameters except `is_gray`.

### GaData
Class for holding and managing data related to a genetic algorithm run. Supports the following parameters:
- `num_generations (int)` - number of generations;
- `children_percent (float, default: 0.95)` - percent of children in new generation;
- `early_stop (int, default: 10)` - early stopping criteria, number of generation without improve.

Attributes:
- `idx_generation (int)` - index of the current generation;
- `num_generation_no_improve (int)` - number of consecutive generations with no improvement;
- `population (BasePopulation)` - current population of individuals;
- `parents (BasePopulation)` - selected parent individuals for crossover;
- `children (BasePopulation)` - offspring individuals produced by crossover;
- `historical_best (list)` - list of historical best scores for each generation;
- `historical_mediocre (list)` - list of historical average scores for each generation;
- `historical_worst (list)` - list of historical worst scores for each generation;
- `best_solution (dict)` - dictionary representing the best individual solution found so far;
- `gen_pool (tuple)` - in case of categorical GA is tuple of possible values for each gene.

### MultiGaData
Child class of GaData, implementing its functionality for multi-objective optimization. Supports all the attributes
of the GaData class.


### NewGeneration
Class for creating a new generation of individuals in a genetic algorithm. Supports the following parameter:
- `transfer_parents (str, default: 'best')` - strategy for transferring certain amount of parents to the next generation. Can be 'best' or 'random'.

### Classes for penalties
Class for creating and calculating penalty for conditional optimization.

- StaticPenalty()
- DynamicPenalty()
- AdaptivePenalty()

Only 2 types of conditional: `g(x) <= 0` or  `h(x) == 0`.

Example: 
```python
my_obj_func(x1, x2):
    return x1**2 + x2**2, 1-x1+x2, x1+x2
dp = DynamicPenalty()
HyperbolaFitness(obj_function=my_func, obj_value=0, penalty=dp,
                 conditions=['optimize', '<=', '!='])
```

### HyperbolaFitness
Class for calculating fitness value using the hyperbola approach. Supports the following parameters:
- `obj_function (Callable)` - object function with 1 or 2 arguments, my_func(gens: list) or
                             my_func(input_data: Any, gens: list);
- `obj_value (int | float, default: None)` - if object value exists, GA will optimize to the value,
                          else GA will optimize to min;
- `input_data (Any, default: None)` - argument for object function, you can pass any additional information to object function;
- `penalty (class BasePenalty, default: None)` - subclass of BasePenalty(), used for conditional optimization;
- `conditions: (list of strings, default: None)` - 3 value can be use: 'optimize', '<=', '!='.
### Classes for populations

- BinaryPopulation() 
- BinaryGrayPopulation()
- CatPopulation()
- OrderCatPopulation()

All classes support the following parameters:
- `num_individ (int)` - number of individuals in generation (size of population);
- `gens (tuple)` - controls the gens type;
- `input_population (list[list], default: None)` - optional input population to be used for initialization.


### Classes for selection methods

For all types GA except VEGA:

- BalancedSelection()
- RankedSelection()
- TournamentSelection() - supports `tournament_size` parameter with default value - 3.

For VEGA:

- VEGABalancedSelection()
- VEGARankedSelection()
- VEGATournamentSelection()

### Classes for crossover methods

For binary and categorical GA:

 - OnePointCrossover()
 - TwoPointCrossover()
 - UniformCrossover()

For combinatory GA:

- OrderCrossover()

### Classes for mutation methods

For binary GA:

- BinStringMutation()

For combinatory GA:

- InversionMutation()
- MovementMutation()
- ShiftMutation()
- SwapMutation()

For categorical GA:

- CategoricalMutation()

This classes support one parameter - `mutation_lvl`. Can be string ('weak', 'normal', 'strong') or a float from 0 to 1. Default value - 'normal'.

### Random seed
For random seed use `baumeva.generator.rnd_seed = number` before GA implementation, where `number` is any integer value.



## License

The BaumEvA library is distributed under the MIT License. See the [LICENSE](https://github.com/DateOrMage/BaumEvolutionAlgorithms/blob/master/LICENSE.txt) file for more information.

## Contribution

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue on the [GitHub repository](https://github.com/DateOrMage/BaumEvolutionAlgorithms).

## Contact

For any inquiries or questions, you can reach out to the author via email at [vatutu@gmail.com](mailto:vatutu@gmail.com).
