# -----------------------------------------------------------
# © 2023 Alexander Isaychikov
# Released under MIT License
# Minsk, Belarus
# email alipheesa@gmail.com
# -----------------------------------------------------------

class Variable:
    """
    The Variable class instances serve as building blocks in computation graph

    Parameters
    ----------
    idf : str
        Every Variable class instance must have its identifier (see examples below)
    _prev : list
        List of previous node(s) in computation graph
    _operand_list : list
        List of all registered operands in computation graph

    Variables
    ---------
    idf : str
        Stores identifier
    _prev : list
        Stores tuple of previous nodes
    _operand_list : list
        Stores operand list

    Notes
    -----
    Note that Variable's __call__ function receives not a list, but
    a dict with every operand's identifier as key and 0/1 as value
    example: {'A':0, 'B':1, 'C':0}
    """

    def __init__(self, idf, _prev=None, _operand_list=None):

        self.idf = idf
        self._prev = _prev

        if _operand_list is None:
            if idf not in ['&', '|', '~']:
                self._operand_list = [idf]
        else:
            self._operand_list = list(set(_operand_list))

        self._operand_list.sort()

    def __call__(self, bool_dict):
        if self.idf == '&':
            return self._prev[0](bool_dict) & self._prev[1](bool_dict)
        elif self.idf == '|':
            return self._prev[0](bool_dict) | self._prev[1](bool_dict)
        elif self.idf == '~':
            return 0 if self._prev[0](bool_dict) else 1
        else:
            return bool_dict[self.idf]

    def __or__(self, other):
        return Variable('|', [self, other], (self._operand_list + other._operand_list))

    def __and__(self, other):
        return Variable('&', [self, other], (self._operand_list + other._operand_list))

    def __invert__(self):
        return Variable('~', [self], self._operand_list)

    def get_operand_list(self):
        return self._operand_list

