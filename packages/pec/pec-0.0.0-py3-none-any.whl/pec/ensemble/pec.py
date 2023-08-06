import hashlib
import inspect
import signal
import time
from multiprocessing import Lock, SimpleQueue

import numpy as np
import pandas as pd
from sklearn.utils._param_validation import (Integral, Interval, StrOptions,
                                             validate_params)

from pec.clustering.kmeans import ProgressiveKMeansRun
from pec.utils.seed import RandomStateGenerator

from ..decision.inertia_based import InertiaBased_ProgressiveDecisionWorker
from ..progression.observable import ProgressionObservable
from ..progression.observer import ProgressionObserver
from ..utils.array import SharedArray
from ..utils.labels import best_labels_dtype


class _ProgressiveEnsembleClustering(ProgressionObservable):
    """Progressive Ensemble Clustering

    ----------
    parameters :

        data : array-like or sparse matrix.

        n_clusters : number of clusters >= 2.

        n_runs : number of parallel runs to execute >= 2.

        alg : algorithm to use, string in {'k-means', 'k-means++'}.

        decision : decision to use, string in {'inertia', 'hgpa', 'mcla'}.

        random_state : seed for random generator. An integer used as seed generator, or an integer array of len n_runs.
        In the case of an array, each element is used as seed for the different runs.
    """

    @validate_params(
        {
            'data': ['array-like', 'sparse matrix'],
            'n_clusters': [Interval(Integral, 2, None, closed='left')],
            'n_runs': [Interval(Integral, 2, None, closed='left')],
            'algo': [StrOptions({'k-means', 'k-means++'})],
            'decision': [StrOptions({'inertia', 'hgpa', 'mcla'})]
        }
    )
    def __init__(self, data, n_clusters=2, n_runs=4, alg='k-means', decision='inertia', random_state=None,
                 observer=None, id=None, verbose=False, instance_name=None):

        super().__init__(observer)
        self.data = data.to_numpy() if isinstance(data, pd.DataFrame) else data
        self.id = id if id is not None else self.__get_id(self.data, n_clusters, n_runs, alg, decision, random_state)

        self.n_entries = data.shape[0]
        self.n_clusters = n_clusters
        self.n_runs = n_runs
        self.alg = alg
        self.decision = decision
        self.instance_name = instance_name if instance_name is not None else self.__get_instance_name()
        self.random_state = random_state
        self.verbose = verbose

        self.__active = False
        self.__data_shm, self.__data_sh_obj = SharedArray.create(self.data)
        self.__partitions_shm, self.__partitions_sh_obj = SharedArray.create(
            np.full((self.n_runs, self.data.shape[0]), 0, dtype=best_labels_dtype(self.n_clusters))
        )

        if isinstance(self.random_state, list):
            self.__random_state_arr = self.random_state
            if len(self.__random_state_arr) != self.n_runs:
                raise RuntimeError(f'random_state must be a list of integer of len {self.n_runs}')
        else:
            self.__random_state_arr = RandomStateGenerator(self.random_state).get(self.n_runs)

        self.__clustering_run_arr = None
        self.__decision_worker = None
        self.__clustering_runs_results_queue_arr = [SimpleQueue() for _ in range(self.n_runs)]
        self.__clustering_runs_ack_queue_arr = [SimpleQueue() for _ in range(self.n_runs)]
        self.__clustering_runs_lock_arr = [Lock() for _ in range(self.n_runs)]
        self.__partial_results_queue = SimpleQueue()

        self.__prevResult = None  # previous partial result
        self.lastResult = None

    def __get_id(self, data, n_clusters, n_runs, alg, decision, random_state):
        """Generates a unique id of this pec instance"""
        rawString = "||||".join([
            str(hashlib.sha256(data.tobytes()).hexdigest()),
            str(n_clusters),
            str(n_runs),
            str(alg),
            str(decision),
            str(random_state)
        ])
        return str(hashlib.sha256(rawString.encode()).hexdigest())

    def __get_instance_name(self):
        if self.alg == "k-means" and self.decision == "inertia":
            return 'I-PecK'
        elif self.alg == "k-means++" and self.decision == "inertia":
            return 'I-PecK++'
        else:
            raise RuntimeError(f"Not yet implemented alg-decision pair: '{self.alg} -- {self.decision}'.")

        """elif self.alg == "k-means" and self.decision == "hgpa":
                    return 'HGPA-PecK'
                elif self.alg == "k-means++" and self.decision == "hgpa":
                    return 'HGPA-PecK++'
                elif self.alg == "k-means" and self.decision == "mcla":
                    return 'MCLA-PecK'
                elif self.alg == "k-means++" and self.decision == "mcla":
                    return 'MCLA-PecK++'"""

    def __new_InertiaBased_ProgressiveDecisionWorker(self):
        return InertiaBased_ProgressiveDecisionWorker(
            self.id, self.__data_sh_obj, self.__partitions_sh_obj, self.n_clusters, self.__partial_results_queue,
            self.__clustering_runs_results_queue_arr, self.__clustering_runs_ack_queue_arr,
            self.__clustering_runs_lock_arr,
            verbose=self.verbose
        )

    """def __new_HGPA_ProgressiveDecisionWorker(self):
        raise RuntimeError('TODO')
        return HGPA_ProgressiveDecisionWorker(
            self.__data_sh_obj, self.__partitions_sh_obj, self.n_clusters, self.__partial_results_queue, 
            self.__clustering_runs_results_queue_arr, self.__clustering_runs_ack_queue_arr, self.__clustering_runs_lock_arr,
            start_time=self.__start_time, verbose=self.verbose
        )"""

    """def __new_MCLA_ProgressiveDecisionWorker(self):
        raise RuntimeError('TODO')
        ## uncomment if using mcla-hgpa
        return MCLA_ProgressiveDecisionWorker(
            self.__data_sh_obj, self.__partitions_sh_obj, self.n_clusters, self.__partial_results_queue, 
            self.__clustering_runs_results_queue_arr, self.__clustering_runs_ack_queue_arr, self.__clustering_runs_lock_arr,
            start_time=self.__start_time, verbose=self.verbose
        )"""

    def __new_arr_ProgressiveKMeansRun(self, alg, **kwargs):
        arr = []
        for i in range(self.n_runs):
            kr = ProgressiveKMeansRun(i, self.__data_sh_obj, self.__partitions_sh_obj, self.n_clusters,
                                      self.__clustering_runs_results_queue_arr[i],
                                      self.__clustering_runs_ack_queue_arr[i], self.__clustering_runs_lock_arr[i],
                                      alg=alg, random_state=self.__random_state_arr[i],
                                      verbose=self.verbose, **kwargs)
            arr.append(kr)
        return arr

    def __manage_ctrlC(self, *args):
        """ Manage Ctrl_C keyboard event """
        self.__clean()
        print(f"[{self.__class__.__name__}] Received Ctrl_C keyboard event.")

    def __clean(self):
        """ Close shared resources """
        if self.__decision_worker is not None: self.__decision_worker.kill()
        if self.__clustering_run_arr is not None:
            for cr in self.__clustering_run_arr: cr.kill()

        self.__clustering_runs_results_queue_arr = None
        self.__clustering_runs_ack_queue_arr = None
        self.__clustering_runs_lock_arr = None
        self.__partial_results_queue = None

        self.__data_shm.close()
        self.__data_shm.unlink()
        self.__partitions_shm.close()
        self.__partitions_shm.unlink()

    def start(self):
        self.__active = True
        self.__exec()
        return self

    def stop(self):
        self.__active = False

    def __on_end(self):
        pass

    def __exec(self):
        ###
        ### instantiate workers
        ###
        if self.alg == "k-means" and self.decision == "inertia":
            self.__decision_worker = self.__new_InertiaBased_ProgressiveDecisionWorker()
            self.__clustering_run_arr = self.__new_arr_ProgressiveKMeansRun(self.alg)
        elif self.alg == "k-means++" and self.decision == "inertia":
            self.__decision_worker = self.__new_InertiaBased_ProgressiveDecisionWorker()
            self.__clustering_run_arr = self.__new_arr_ProgressiveKMeansRun(self.alg)
        else:
            raise RuntimeError(f"Not yet implemented alg-decision pair: '{self.alg} -- {self.decision}'.")

        """elif self.alg == "k-means" and self.decision == "hgpa":
                    self.__decision_worker = self.__new_HGPA_ProgressiveDecisionWorker()
                    self.__clustering_run_arr = self.__new_arr_ProgressiveKMeansRun(self.alg)
                elif self.alg == "k-means++" and self.decision == "hgpa":
                    self.__decision_worker = self.__new_HGPA_ProgressiveDecisionWorker()
                    self.__clustering_run_arr = self.__new_arr_ProgressiveKMeansRun(self.alg)
                elif self.alg == "k-means" and self.decision == "mcla":
                    self.__decision_worker = self.__new_MCLA_ProgressiveDecisionWorker()
                    self.__clustering_run_arr = self.__new_arr_ProgressiveKMeansRun(self.alg)
                elif self.alg == "k-means++" and self.decision == "mcla":
                    self.__decision_worker = self.__new_MCLA_ProgressiveDecisionWorker()
                    self.__clustering_run_arr = self.__new_arr_ProgressiveKMeansRun(self.alg)"""

        ###
        ### start workers
        ###
        self.__decision_worker.start()
        for cr in self.__clustering_run_arr: cr.start()
        try:
            signal.signal(signal.SIGINT, self.__manage_ctrlC)  # Manage Ctrl_C keyboard event
        except ValueError as e:
            pass
        ### waiting for partial results
        while self.__active:
            result = self.__partial_results_queue.get()
            # update timestamp of result. original timestamp is when the result was generated, but some delay can appear when is recieved here
            result.info.timestamp = round(time.time(), 4)

            # update previous and current result
            previousResult = self.__prevResult
            self.__prevResult = result
            currentResult = result

            # check if early termination
            currentResult.info.is_last_et = self._checkIfEarlyTermination(self.data, previousResult, currentResult)
            if currentResult.info.is_last or currentResult.info.is_last_et:
                self.__active = False

            # notify the partial result
            self.lastResult = currentResult
            self._notifyPartialResult(self.data, previousResult, currentResult)

        ###
        ### process completed
        ###
        self.__on_end()
        self.__clean()
        if self.verbose: print(f"[{self.__class__.__name__}] terminated.")
