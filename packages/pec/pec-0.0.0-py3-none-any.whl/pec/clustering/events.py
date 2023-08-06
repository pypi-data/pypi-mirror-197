import time

from sklearn.utils import Bunch


class Event(Bunch):
    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)


class IterationResultEvent(Event):
    def __init__(self, timestamp=None, run_id=None, iteration=None, is_last=None, inertia=None, **kwargs):
        super().__init__(
            "IterationResultEvent",
            timestamp=timestamp,
            run_id=run_id,
            iteration=iteration,
            is_last=is_last,
            inertia=inertia,
            **kwargs
        )


class RunResultEvent(Event):
    def __init__(self, timestamp=None, run_id=None, iteration=None, is_last=None, inertia=None, labels=None, clustering_time=None,
                 **kwargs):
        super().__init__(
            "RunResultEvent",
            timestamp=timestamp,
            run_id=run_id,
            iteration=iteration,
            is_last=is_last,
            inertia=inertia,
            labels=labels,
            clustering_time=clustering_time,
            **kwargs
        )


class Ack(Event):
    def __init__(self):
        super().__init__(
            "AckEvent",
            timestamp=time.time()
        )
