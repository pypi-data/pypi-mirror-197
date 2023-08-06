import os
import time
from multiprocessing import Process

from pec.clustering.events import Ack, IterationResultEvent, RunResultEvent
from pec.clustering.sklearn_cluster_kmeans import KMeans
from pec.utils.labels import best_labels_dtype


class MonolithicKMeansRun:
    """Monolithic KMeans Run, no partial results, only a single final result"""

    def __init__(self, id, data, n_clusters, random_state=None, alg="k-means", max_iter=299, tol=1e-4, verbose=False,
                 **kwargs):
        self.id = id
        self.data = data
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.alg = alg
        self.max_iter = max_iter
        self.tol = tol
        self.verbose = verbose
        self.labels_dtype = best_labels_dtype(self.n_clusters)

        self.start_time = None
        self.run_result_event = None

    def run(self):

        # partial result fn, save only the final result
        def fn(r):
            if r.is_last:
                self.run_result_event = RunResultEvent(
                    timestamp=time.time(),
                    run_id=self.id,
                    iteration=r.iteration,
                    is_last=r.is_last,
                    inertia=r.inertia,
                    labels=r.labels.astype(self.labels_dtype),
                    clustering_time = time.time() - self.start_time
                )

        self.start_time = time.time()
        kmean = None
        if self.alg == "k-means":
            kmeans = KMeans(n_clusters=self.n_clusters, n_init=1, max_iter=self.max_iter, init="random",
                            random_state=self.random_state, tol=self.tol, algorithm='elkan')
            kmeans.fit(self.data, on_partial_result=fn)
        elif self.alg == "k-means++":
            kmeans = KMeans(n_clusters=self.n_clusters, n_init=1, max_iter=self.max_iter, init="k-means++",
                            random_state=self.random_state, tol=self.tol, algorithm='elkan')
            kmeans.fit(self.data, on_partial_result=fn)
        else:
            raise RuntimeError(f"[{self.__class__.__name__} #{self.id}] Undefined alg type '{self.alg}'.")

        return self.run_result_event


class ProgressiveKMeansRun(Process):
    """ Progressive KMeans Clustering Run """

    def __init__(self, id, shared_data, shared_partitions, n_clusters, results_queue, ack_queue, lock,
                 random_state=None, alg="k-means", max_iter=299, tol=1e-4, verbose=False, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.shared_data = shared_data
        self.shared_partitions = shared_partitions
        self.n_clusters = n_clusters

        self.results_queue = results_queue
        self.ack_queue = ack_queue
        self.lock = lock

        self.random_state = random_state
        self.alg = alg
        self.max_iter = max_iter
        self.tol = tol
        self.verbose = verbose
        self.labels_dtype = best_labels_dtype(self.n_clusters)

    def run(self):
        if self.verbose: print(f"[{self.__class__.__name__}#{self.id}] started with pid={os.getpid()}.")
        shm_data, data = self.shared_data.open()
        shm_partitions, partitions = self.shared_partitions.open()

        # partial results fn
        def fn(r):
            labels = r.labels.astype(self.labels_dtype)

            partitions[self.id, :] = labels
            it_event = IterationResultEvent(
                timestamp=time.time(),
                run_id=self.id,
                iteration=r.iteration,
                is_last=r.is_last,
                inertia=r.inertia
            )
            self.results_queue.put(it_event)
            if not r.is_last:
                recv_ack = self.ack_queue.get()
                if not isinstance(recv_ack, Ack): raise RuntimeError(
                    f"[{self.__class__.__name__}] Expected an AckEvent, got {recv_ack.__class__.__name__}.")

        ####
        if self.alg == "k-means":
            kmeans = KMeans(n_clusters=self.n_clusters, n_init=1, max_iter=self.max_iter, init="random",
                            random_state=self.random_state, tol=self.tol, algorithm='elkan')
            kmeans.fit(data, on_partial_result=fn)
        elif self.alg == "k-means++":
            kmeans = KMeans(n_clusters=self.n_clusters, n_init=1, max_iter=self.max_iter, init="k-means++",
                            random_state=self.random_state, tol=self.tol, algorithm='elkan')
            kmeans.fit(data, on_partial_result=fn)
        else:
            raise RuntimeError(f"[{self.__class__.__name__} #{self.id}] Undefined alg type '{self.alg}'.")

        shm_data.close()
        shm_partitions.close()
        if self.verbose: print(f"[{self.__class__.__name__} #{self.id}] terminated.")
