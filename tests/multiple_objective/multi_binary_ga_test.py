from baumeva import FFGA, VEGA
import math
import time


class timex:
    def __enter__(self):
        # Фиксация времени старта процесса
        self.t = time.time()
        return self

    def __exit__(self, type, value, traceback):
        # Вывод времени работы
        print('Время обработки: {:.2f} с'.format(time.time() - self.t))


def griewank_func(value_list):
    res_sum = 0
    res_mpl = 1
    for i, value in enumerate(value_list):
        res_sum += (value*value) / 4000
        res_mpl *= math.cos(value/math.sqrt(i+1))
    return res_sum - res_mpl + 1


def sum_of_squares(value_list):
    result = 0
    for value in value_list:
        result += value*value
    return result

# --------------------- http://www.vestnik.vsu.ru/pdf/analiz/2010/02/2010-02-06.pdf ----------------------------------


def linear_f1(x: list) -> float:
    return -4*x[0]-2*x[1]


def linear_f2(x: list) -> float:
    return -2*x[0]-4*x[1]


def linear_f3(x: list) -> float:
    return -3*x[0]-9*x[1]


def linear_f4(x: list) -> float:
    return -8*x[0]-2*x[1]


def linear_f5(x: list) -> float:
    return -4*x[0]+x[1]


def linear_f6(x: list) -> float:
    return -3*x[0]+2*x[1]


def linear_f7(x: list) -> float:
    return 2*x[0] - 4*x[1]


def linear_f8(x: list) -> float:
    return 3*x[0] - x[1]


def linear_f9(x: list) -> float:
    return 4*x[0] + 3*x[1]


def multilinear_conditions(x: list) -> tuple:
    return linear_f1(x), linear_f2(x), linear_f3(x), linear_f4(x), linear_f5(x), linear_f6(x), linear_f7(x), \
        linear_f8(x), linear_f9(x), 2*x[0]+3*x[1], -x[0]+3*x[1], 2*x[0]-x[1], -x[0], -x[1]

# ---------------------------- https://github.com/P-N-Suganthan/2021-RW-MOP/blob/main/RWMOP.pdf -----------------------
# 2.1.3 Two Bar Truss Design (page 5)


def rcm03(x: list) -> tuple:
    """
    conditions=['optimize']*2 + ['<=']*3
    gens=((0.00001, 100, 0.01), (0.00001, 100, 0.01), (1, 3, 0.01))
    """
    f1 = x[0]*math.sqrt(16+x[2]**2) + x[1]*math.sqrt(1+x[2]**2)
    f2 = 20*math.sqrt(16+x[2]**2) / (x[2]*x[0])
    g1 = f1 - 0.1
    g2 = f2 - 10000
    g3 = 80*math.sqrt(1+x[2]**2) / (x[2]*x[1]) - 10000
    return f1, f2, g1, g2, g3


# --------------------------- https://pymoo.org/problems/ ------------------------------------------------------------
def zdt1(x: list) -> tuple:
    """
    conditions=['optimize']*2
    gens=((0, 1, 0.01),)*30
    """
    f1 = x[0]
    g = 1 + 9 / (len(x) - 1) * sum(x[1:])
    h = 1 - math.sqrt(f1/g)
    f2 = g * h

    return f1, f2


def zdt2(x: list) -> tuple:
    """
    conditions=['optimize']*2
    gens=((0, 1, 0.01),)*30
    """
    f1 = x[0]
    g = 1 + 9 / (len(x) - 1) * sum(x[1:])
    h = 1 - (f1/g)**2
    f2 = g * h

    return f1, f2


def zdt3(x: list) -> tuple:
    """
    conditions=['optimize']*2
    gens=((0, 1, 0.01),)*30
    """
    f1 = x[0]
    g = 1 + 9 / (len(x) - 1) * sum(x[1:])
    h = 1 - math.sqrt(f1/g) - (f1/g)*math.sin(10*math.pi*f1)
    f2 = g * h

    return f1, f2


def zdt4(x: list) -> tuple:
    """
    conditions=['optimize']*2
    gens=tuple([(0, 1, 0.01)]+[(-10, 10, 0.01)]*10)
    """
    f1 = x[0]

    s = 0
    for xi in x[1:]:
        s += xi**2 - 10*math.cos(4*math.pi*xi)

    g = 1 + 10*(len(x) - 1) + s
    h = 1 - math.sqrt(f1/g)
    f2 = g * h

    return f1, f2


# ------------------------------------- some simple quadrics -----------------------------------------------------------

def quadratic(x: list) -> tuple:
    """
    conditions=['optimize']*3
    gens=tuple([(0, 100, 0.01)]*2)
    """
    return (x[0] - 2)**2 + (x[1] - 2)**2, x[0]*x[0] + x[1]*x[1], (x[0] - 4)**2 + (x[1] - 1)**2


moga = VEGA(num_generations=100,
            num_individ=100,
            gens=((0, 1, 0.01),)*30,
            obj_function=zdt1,
            # obj_value=0,
            conditions=['optimize']*2,
            # penalty=DynamicPenalty(),
            is_gray=False,
            mutation_lvl=0.05,
            early_stop=None)

with timex():
    ga_data = moga.optimize()
# ga_data_conditions = bin_ga_conditions.optimize()
