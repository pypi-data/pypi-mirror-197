import numpy as np
from sklearn.utils import check_random_state
from sklearn.utils._param_validation import (Integral, Interval, StrOptions,
                                             validate_params)


class RandomStateGenerator:
    def __init__(self, random_state=None):
        self.random_state = random_state

    @validate_params(
        {
            'size': [Interval(Integral, 1, None, closed='left')]
        }
    )
    def get(self, size=1):
        result = check_random_state(self.random_state).randint(np.iinfo(np.int32).max, size=size)
        if self.random_state is not None:
            result[0] = int(self.random_state)
        return result
