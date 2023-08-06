
from .datasets.dataset import DefaultDataset
from .ensemble import I_PecK, I_PecKPP
# HGPA_PecK, HGPA_PecKPP, MCLA_PecK, MCLA_PecKPP
from .progression.observer import ProgressionObserver
from .utils import ClusteringMetrics, RandomStateGenerator
from .version import __version__


def __checkPythonVersion():
    import sys
    if not (sys.version_info.major == 3 and sys.version_info.minor >= 9):
        current = f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'
        raise RuntimeError(f'The required python version is >= 3.9 while the current python version is {current}')


#__checkPythonVersion()
