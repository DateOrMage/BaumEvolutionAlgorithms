import random
from typing import List, Tuple, Union


def get_real_number_of_points(num_points: int):
    """
    Function for search n: 2**n - 1 >= num_points, where n is number of bits.
    Returns n and real_num_points = 2**n - 1.
    """
    n = 0
    while (2**n - 1) < num_points:
        n += 1

    return n, 2**n - 1


def get_gray_value(value: int):
    """
    Function for coding integer value into graycode
    :param value: input integer value
    :return: graycode in integer type
    """
    return value ^ (value >> 1)


def index_to_binary(value: int, num_bits: int, is_graycode=False):
    """
    Function for coding integer value to binary with definition number of bits.
    Return binary string.
    """
    if is_graycode:
        value = get_gray_value(value)
    bin_string = bin(value)[2:]
    if len(bin_string) > num_bits:
        raise Exception(f'Cannot convert {value} to binary string with current number of bits: {num_bits}')
    elif len(bin_string) < num_bits:
        bin_string = '0'*(num_bits - len(bin_string)) + bin_string
    return bin_string


def get_index_from_gray(gray_value: int):
    """
    Get index of point from gray value.
    :param gray_value: integer
    :return: index of point
    """
    real_value = 0
    while gray_value > 0:
        real_value = real_value ^ gray_value
        gray_value = gray_value >> 1
    return real_value


def get_odd_num_children(num_population: int, percent_children: float):
    """
    Return odd value of children
    """
    num_children = int(num_population * percent_children)
    if (num_children % 2) != 0:
        num_children += 1
    return num_children


def get_result_mutation(probability, sample):
    """
    Return bool value of mutation.
    """
    if random.randint(0, sample-1) < (probability * sample):
        return True
    else:
        return False


def sort_list_with_index(value_list, reverse=True):
    """
    Function for sorting list in decreasing order with saving initial indexes.
    :param value_list: any list with integer or float values.
    :param reverse: bool, True is decrease sort, False is increase sort.
    :return: value_idx_list: sorted list of dicts with 'value' and 'id'.
    """
    value_idx_list = [{'value': x, 'id': i} for i, x in enumerate(value_list)]
    value_idx_list.sort(key=lambda x: x['value'], reverse=reverse)
    return value_idx_list


def get_balanced_selection(scores_list, num_children, selected_idx_list=None):
    if selected_idx_list is None:
        selected_idx_list = []
    sum_scores = sum(scores_list)
    proportional = 0
    proportional_list = [proportional]
    for score in scores_list:
        proportional += score / sum_scores
        proportional_list.append(proportional)
    avg_step = 1 / (len(proportional_list) - 1)
    for j in range(num_children):
        random_value = random.random()
        idx = int(random_value / avg_step)
        while True:
            if random_value >= proportional_list[idx]:
                if random_value <= proportional_list[idx + 1]:
                    selected_idx_list.append(idx)
                    break
                else:
                    idx += 1
            else:
                idx -= 1
    return selected_idx_list


def get_sum_conditional_func(conditional_func: List[Tuple], gens: list, power: Union[int, float] = 1):
    """
    :param conditional_func: list[tuple], array of tuples, example:
                                  [(my_func_0, 'equal'),
                                   (my_func_1, 'inequal')]
    :param gens: list, array of real gens
    :param power: int, power of every function
    :return: total_res: float, f1**power + f2**power + ... + fn**power, where n - len(conditional_func_list)
    """
    total_res = 0
    for cfl_tuple in conditional_func:
        if cfl_tuple[1] == "equal":
            if cfl_tuple[2]:
                res = abs(cfl_tuple[0](cfl_tuple[2], gens))
            else:
                res = abs(cfl_tuple[0](gens))
        elif cfl_tuple[1] == "inequal":
            if cfl_tuple[2]:
                res = max(0, cfl_tuple[0](cfl_tuple[2], gens))
            else:
                res = max(0, cfl_tuple[0](gens))
        else:
            raise Exception(f'Unexpected type of conditional function: {cfl_tuple[1]}.'
                            f' Please select "equal" or "inequal"')
        total_res += res**power
    return total_res


if __name__ == '__main__':
    # print(get_real_number_of_points(10000000000000000000))
    # print(get_real_number_of_points_2(10000000000000000000))
    # print(get_index_from_gray(29))  # 11101 -> 22 (10110)
    # print(index_to_binary(8, 5))
    # print(get_result_mutation(0.888, 10000))
    # print(sort_list_with_index([564, 123, 11, 3, -9, 0]))
    def my_func(x_list):
        val = 0
        for x in x_list:
            val += x
        return val

    print(get_sum_conditional_func([(my_func, 'equal'), (my_func, 'inequal')], gens=[1, 2, 3], power=2))

