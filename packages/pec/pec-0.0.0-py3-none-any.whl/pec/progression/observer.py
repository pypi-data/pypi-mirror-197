from abc import ABC, abstractmethod


class ProgressionObserver(ABC):
    """
    The ProgressionObserver interface declares the onPartialResult method, called by the PEC Instance.
    """
    def __init__(self):
        pass

    @abstractmethod
    def isEarlyTermination(self, data, iteration, previousResult, currentResult):
        """
        Receive the iteration number, previousResult and currentResult. The function musts return a boolean indicating
        if the early termination occurs at the end of the current iteration. In case of True, the clustering process stops.
        \n\n
        This function is called, at each iteration, from the second one (iteration==1) because the first iteration (iteration==0) has not a previousResult.
        It has available the parameter data, which is the dataset used for clustering as numpy matrix.
        """
        pass

    @abstractmethod
    def onPartialResult(self, data, iteration, currentResult):
        """
        Receive a partialResult (instance of pec.PartialResult) and the current iteration number.
        Iterations start from 0.
        It has available the parameter data, which is the dataset used for clustering as numpy matrix.
        """
        pass
