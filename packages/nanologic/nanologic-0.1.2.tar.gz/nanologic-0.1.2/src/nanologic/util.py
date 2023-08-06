# -----------------------------------------------------------
# © 2023 Alexander Isaychikov
# Released under MIT License
# Minsk, Belarus
# email alipheesa@gmail.com
# -----------------------------------------------------------

import numpy as np
import math
import itertools


def _cartesian(arrays):
    """
    Computes all existing combinations of given arrays
    Parameters
    ----------
    arrays : list
        List of arrays to combine
    Returns
    -------
    list
        List of all combinations
    """

    arrays = [np.asarray(a) for a in arrays]
    shape = (len(x) for x in arrays)

    ix = np.indices(shape, dtype=int)
    ix = ix.reshape(len(arrays), -1).T

    for n, arr in enumerate(arrays):
        ix[:, n] = arrays[n][ix[:, n]]

    return ix


def _expand_vector_to_table(vector):
    """
    Expands vector to truth table, expects vector length to be in set of power of two values
    """
    length = len(vector)
    if math.log(length, 2) != int(math.log(length, 2)):
        raise Exception('Log[2] of input vector\'s length must be integer, not float')

    operand_count = int(math.log(length, 2))
    lists = _cartesian([[0, 1] for _ in range(operand_count)])
    output = [list(x) + y for x, y in zip(lists, vector)]
    return output


def _get_sorted_input(input_list):
    """
    Split input list by amount of true values (1) in each combination
    Parameters
    ----------
    input_list : list
        Matrix (list of lists) of combinations
    Returns
    -------
    list
        list of combination Matrices
    """
    input_list = np.array(input_list)
    n = len(input_list[0])
    sum_list = (input_list == 1).sum(axis=1)
    sorted_list = []

    for i in range(n + 1):
        temp = input_list[sum_list == i]
        sorted_list.append(list(temp))
    sorted_list.append([])

    return sorted_list


def _implicant_forward(input_list, mint_to_i_dict=None):
    """
    Messy function that makes an iteration according to Quine–McCluskey algorithm
    Parameters
    ----------
    input_list : list
        list of combination Matrices, where combinations are splitted
        according to the amount of true values (1) in them
    mint_to_i_dict : dict
    Returns
    -------
    list, dict
        list of combinations
        dict of minterms
    Notes
    -----
    Forwards input list and maps calculated combinations into minterm indices,
    outputted minterm dict is used afterwards to map reduced minterm list back into
    implicant list
    """

    def _get_operand_count():
        return max([max([len(y) for y in x]) for x in input_list if ([len(y) for y in x]) != []])

    if mint_to_i_dict is None:
        mint_to_i = {tuple(v): tuple([k]) for k, v in
                     enumerate(_cartesian([[0, 1] for _ in range(_get_operand_count())]))}
    else:
        mint_to_i = mint_to_i_dict

    output = []
    output_minterm = mint_to_i if mint_to_i_dict is None else mint_to_i_dict

    for j in range(len(input_list) - 1):
        for x in input_list[j]:

            is_combinable = False

            for y in input_list[j + 1]:
                def _handle_combination():
                    counter = 0
                    idx = 0
                    comb = list(y)
                    for i in range(len(x)):
                        if y[i] not in [x[i]]:
                            counter += 1
                            idx = i
                    if counter == 1:
                        comb[idx] = -1
                        if comb not in output:
                            output.append(comb)
                            output_minterm[tuple(comb)] = tuple(set([k for k in mint_to_i[tuple(x)]] +
                                                                    [k for k in mint_to_i[tuple(y)]]))
                        is_combinable = True

                _handle_combination()

            if not is_combinable:
                output.append(list(x))

    return output, output_minterm


def _remove_implicant_duplicates(input_list):
    """
    Recieves a list of implicants and removes duplicate implicants
    of smaller size
    Parameters
    ----------
    input_list : list
        list of implicants
    Returns
    -------
    list
        reduced list of implicants
    """
    output = []
    for x in input_list:
        is_unique = True
        for y in input_list:
            if x == y:
                continue
            if is_unique == False:
                continue
            counter_01 = 0
            counter_01m1 = 0
            counter_m101 = 0
            for i in range(len(x)):
                if x[i] == y[i]:
                    continue
                elif x[i] != -1 and y[i] != -1:
                    counter_01 += 1
                elif x[i] == -1:
                    counter_01m1 += 1
                elif y[i] == -1:
                    counter_m101 += 1

            if counter_01 == 0 and counter_01m1 == 0 and counter_m101 > 0:
                is_unique = False

        if is_unique == True:
            output.append(x)

    return output


def _remove_minterm_duplicates(input_list, minterm_dict):
    """
    Truncates minterm dict by removing keys that are not in implicant list
    """
    return {k: v for k, v in minterm_dict.items() if list(k) in input_list}


def _get_implicant_list(input_list):
    """
    Iterates according to Quine–McCluskey algorithm multiple times,
    outputs implicant list and minterm dict
    Combines all declared above functions
    """
    minterm_dict = None
    for i in range(len(input_list[0])):
        input_list, minterm_dict = _implicant_forward(_get_sorted_input(input_list), minterm_dict)

    output_list = _remove_implicant_duplicates(input_list)
    output_minterm = _remove_minterm_duplicates(output_list, minterm_dict)

    return output_list, output_minterm


def _get_reduced_implicant_list(input_list):
    """
    Reduces implicant list to contain all minterms,
    outputs the smallest minterm combination
    """
    input_list, minterm_dict = _get_implicant_list(input_list)
    minterm_set = set([y for x in minterm_dict.values() for y in x])
    key_combinations = []
    value_combinations = []

    for length in range(len(input_list[0]) + 1):
        for combination in itertools.combinations(list(minterm_dict.keys()), length):
            key_combinations.append(combination)
        for combination in itertools.combinations(list(minterm_dict.values()), length):
            value_combinations.append(set([y for x in combination for y in x]))

    output = [x for i, x in enumerate(key_combinations) if value_combinations[i] == minterm_set]
    if len(output) == 0:
        return []
    output = [x for x in output if len(x) == min([len(y) for y in output])]
    output = [list(x) for x in output[0]]

    return output
