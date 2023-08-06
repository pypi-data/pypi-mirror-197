# -----------------------------------------------------------
# © 2023 Alexander Isaychikov
# Released under MIT License
# Minsk, Belarus
# email alipheesa@gmail.com
# -----------------------------------------------------------

from src.util import _cartesian, _get_reduced_implicant_list, _expand_vector_to_table
from src.Variable import Variable


def get_truth_table(function):
    """
    Computes truth table of given logical function, outputs
    list of lists with size of 2^n, where n is size of functions'
    operand list. Each list contains operand values of certain
    combination and function output, with operand's value position
    corresponding to its position in Variable's sorted operand list

    Parameters
    ----------
    function : Variable
        Logical function represented as computation graph

    Returns
    -------
    list
        Matrix (list of lists) representing truth table

    """

    output = list()
    operand_list = function.get_operand_list()
    length = len(operand_list)

    def _get_bool_dict_list():
        """
        Short function to put every combination into required dict format
        """
        lists = _cartesian([[0, 1] for _ in range(length)])
        dicts = []
        for j in range(len(lists)):
            dict_entry = {operand_list[i]: lists[j][i] for i in range(length)}
            dicts.append(dict_entry)
        return dicts

    dict_list = _get_bool_dict_list()

    for combination in dict_list:
        out = []
        for value in combination.values():
            out.append(value)
        out.append(function(combination))
        output.append(out)

    return output


def print_truth_table(function):
    """
    Simple function to print truth table from a given function
    """
    table = get_truth_table(function)

    operand_list = function.get_operand_list()
    length = len(operand_list)

    def _get_operand_string():
        out = ""
        for x in operand_list:
            out += x + ' '
        out += 'f('
        for i, x in enumerate(operand_list):
            if i < length - 1:
                out += x + ', '
            else:
                out += x
        out += ')'
        return out

    print(_get_operand_string())

    for combination in table:
        out = ""
        for v in combination:
            out += str(v) + ' '
        print(out)


def get_index_form(function):
    """
    Computes index form for given function, which basically
    means converting truth table's function outputs into binary
    format and then into decimal

    Parameters
    ----------
    function : Variable
        Logical function represented as computation graph

    Returns
    -------
    int
        Index form of logical function

    """
    table = get_truth_table(function)

    binary = [x[-1] for x in table]

    decimal = sum([x * pow(2, i) for i, x in enumerate(reversed(binary))])

    return decimal


def build_PDNF(value, custom_operands=None):
    """
    Builds Principal Disjunction Normal Form of a given function or truth table

    Parameters
    ----------
    value : Variable/list
        Input function or truth table's single output vector
    custom_operands: list
        Custom operand identifiers (instead of standard A, B, C etc.)

    Returns
    -------
    str
        String representation of PDNF
    """
    if isinstance(value, Variable):
        table = get_truth_table(value)
    else:
        table = _expand_vector_to_table(value)

    if custom_operands is not None:
        operands = custom_operands
    elif isinstance(value, Variable):
        operands = value._operand_list
    else:
        operands = [chr(65 + i) for i in range(len(table[0]) - 1)]

    combinations = [c[:-1] for c in table if c[-1] == 1]
    if len(combinations) == 0:
        return 'PDNF does not exist'
    out = ""

    for i, c in enumerate(combinations):
        def get_minterm_str(combination):
            temp = ""
            for i, operand in enumerate(operands):
                temp += '' if combination[i] == 1 else '~'
                temp += operand
                temp += '&' if i < len(operands) - 1 else ''
            return temp

        out += '(' + get_minterm_str(c) + ')'
        out += ' | ' if i < len(combinations) - 1 else ''

    return out


def build_PCNF(value, custom_operands=None):
    """
    Builds Conjunctive Disjunction Normal Form of a given function or truth table

    Parameters
    ----------
    value : Variable/list
        Input function or truth table's single output vector
    custom_operands: list
        Custom operand identifiers (instead of standard A, B, C etc.)

    Returns
    -------
    str
        String representation of PCNF
    """
    if isinstance(value, Variable):
        table = get_truth_table(value)
    else:
        table = _expand_vector_to_table(value)

    if custom_operands is not None:
        operands = custom_operands
    elif isinstance(value, Variable):
        operands = value._operand_list
    else:
        operands = [chr(65 + i) for i in range(len(table[0]) - 1)]

    combinations = [c[:-1] for c in table if c[-1] == 0]
    if len(combinations) == 0:
        return 'PCNF does not exist'
    out = ""

    for i, c in enumerate(combinations):
        def get_minterm_str(combination):
            temp = ""
            for i, operand in enumerate(operands):
                temp += '' if combination[i] == 0 else '~'
                temp += operand
                temp += '|' if i < len(operands) - 1 else ''
            return temp

        out += '(' + get_minterm_str(c) + ')'
        out += ' & ' if i < len(combinations) - 1 else ''

    return out


def minimize_PDNF(value, custom_operands=None):
    """
    Builds minimization for PDNF of a given function or truth table

    Parameters
    ----------
    value : Variable/list
        Input function or truth table's single output vector
    custom_operands: list
        Custom operand identifiers (instead of standard A, B, C etc.)

    Returns
    -------
    str
        String representation of PDNF minimization
    """
    if isinstance(value, Variable):
        table = get_truth_table(value)
    else:
        table = _expand_vector_to_table(value)

    if custom_operands is not None:
        operands = custom_operands
    elif isinstance(value, Variable):
        operands = value._operand_list
    else:
        operands = [chr(65 + i) for i in range(len(table[0]) - 1)]

    combinations = [c[:-1] for c in table if c[-1] == 1]
    if len(combinations) == 0:
        return 'PDNF minimization does not exist'
    combinations = _get_reduced_implicant_list(combinations)
    if len(combinations) == 0:
        return build_PDNF(value, custom_operands)
    out = ""

    for current_index, combination in enumerate(combinations):
        def get_minterm_str(combination):
            string = ""
            operator_count = len([x for x in combination if x != -1]) - 1
            for i, operand in enumerate(operands):
                string += '~' if combination[i] == 0 else ''
                string += operand if combination[i] != -1 else ''
                string += '&' if (operator_count > 0 and combination[i] != -1) else ''
                if operator_count > 0 and combination[i] != -1:
                    operator_count -= 1

            return string

        out += '(' + get_minterm_str(combination) + ')'
        out += ' | ' if current_index < len(combinations) - 1 else ''

    return out


def minimize_PCNF(value, custom_operands=None):
    """
    Builds minimization for PCNF of a given function or truth table

    Parameters
    ----------
    value : Variable/list
        Input function or truth table's single output vector
    custom_operands: list
        Custom operand identifiers (instead of standard A, B, C etc.)

    Returns
    -------
    str
        String representation of PCNF minimization
    """
    if isinstance(value, Variable):
        table = get_truth_table(value)
    else:
        table = _expand_vector_to_table(value)

    if custom_operands is not None:
        operands = custom_operands
    elif isinstance(value, Variable):
        operands = value._operand_list
    else:
        operands = [chr(65 + i) for i in range(len(table[0]) - 1)]

    combinations = [c[:-1] for c in table if c[-1] == 0]
    if len(combinations) == 0:
        return 'PCNF minimization does not exist'
    combinations = _get_reduced_implicant_list(combinations)
    if len(combinations) == 0:
        return build_PCNF(value, custom_operands)
    out = ""

    for n, c in enumerate(combinations):
        def get_minterm_str(combination):
            string = ""
            operator_count = len([x for x in combination if x != -1]) - 1
            for i, operand in enumerate(operands):
                string += '~' if combination[i] == 1 else ''
                string += operand if combination[i] != -1 else ''
                string += '|' if (operator_count > 0 and combination[i] != -1) else ''
                if operator_count > 0 and combination[i] != -1:
                    operator_count -= 1

            return string

        out += '(' + get_minterm_str(c) + ')'
        out += ' & ' if n < len(combinations) - 1 else ''

    return out
