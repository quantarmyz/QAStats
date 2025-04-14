####
# QUANTARMY 2022 - PRIVATE CODE - ALL RIGTHS RESERVED
# QUANTARMY 2023 - PRIVATE CODE - ALL RIGTHS RESERVED
# QUANTARMY 2024 - GNU PUBLIC LICENSE (ALL SOURCE RELEASED)
# QUANTARMY 2025 - GNU PUBLIC LICENSE - OPEN SOURCE
# by jcx - jcx@quantarmy.com | https://quantarmy.com
####
# Noviembre 2022
# Enero 2023 - 
# Feb 2024 - Update 2.0
# Abril 2025 - Update 3
##### armystats v3

from . import timeseries
from . import stats
from . import reports
from . import randomizer
from . import plots
from . import extension
from . import utils
__all__ = [

    "timeseries",
    "stats",
    "reports",
    "randomizer",
    "plots",
    "extension",
    "utils",
]


from .stats import *
from .utils import *
from .plots import  *
from .reports import *

__all__ = ['stats', 'plots', 'reports', 'utils', 'extend_pandas']

def extend_pandas():
    """
    Extends pandas by exposing methods to be used like:
    df.sharpe(), df.best('day'), ...
    """
    from pandas.core.base import PandasObject as _po
    _po.varusd = stats.var_usd