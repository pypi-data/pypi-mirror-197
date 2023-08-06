# -----------------------------------------------------------
# © 2023 Alexander Isaychikov
# Released under MIT License
# Minsk, Belarus
# email alipheesa@gmail.com
# -----------------------------------------------------------

from .Variable import Variable
from .operations import get_truth_table, print_truth_table, get_index_form, \
    build_PCNF, build_PDNF, minimize_PCNF, minimize_PDNF

__all__ = [
    'Variable',
    'get_truth_table',
    'print_truth_table',
    'get_index_form',
    'build_PCNF',
    'build_PDNF',
    'minimize_PCNF',
    'minimize_PDNF'
]
