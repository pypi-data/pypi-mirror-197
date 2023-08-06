
from . import Variable
from . import util
from . import operations

__all__ = [
    'Variable.Variable',
    'operations.get_truth_table',
    'operations.print_truth_table',
    'operations.get_index_form',
    'operations.build_PCNF',
    'operations.build_PDNF',
    'operations.minimize_PCNF',
    'operations.minimize_PDNF'
]
