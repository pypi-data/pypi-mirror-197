import inspect

from ..ensemble.results import PartialResult
from .observer import ProgressionObserver


def _checkResultsClass(previousResult, currentResult):
    if previousResult is not None and not isinstance(previousResult, PartialResult):
        raise RuntimeError(f'previousResult must be instance of PartialResult')
    if not isinstance(currentResult, PartialResult):
        raise RuntimeError(f'currentResult must be instance of PartialResult')


class ProgressionObservable:
    def __init__(self, observer):
        self.observer = None

        if observer is not None:
            if inspect.isclass(observer):
                self.observer = observer()
                if not isinstance(self.observer, ProgressionObserver):
                    raise RuntimeError(f'observer is not a subclass of ProgressionObserver')
            else:
                if isinstance(observer, ProgressionObserver):
                    self.observer = observer
                else:
                    raise RuntimeError(f'observer is not an instance of ProgressionObserver')

    def _checkIfEarlyTermination(self, data, previousResult, currentResult):
        if self.observer is None:
            return False

        _checkResultsClass(previousResult, currentResult)
        iteration = currentResult.info.iteration

        if iteration > 0:
            et = self.observer.isEarlyTermination(data, iteration, previousResult, currentResult)
            if not isinstance(et, bool):
                raise RuntimeError(f'ProgressionObserver.isEarlyTermination must return a boolean')
            return et
        else:
            return False

    def _notifyPartialResult(self, data, previousResult, currentResult):
        if self.observer is None:
            return

        _checkResultsClass(previousResult, currentResult)
        iteration = currentResult.info.iteration
        self.observer.onPartialResult(data, iteration, currentResult)
