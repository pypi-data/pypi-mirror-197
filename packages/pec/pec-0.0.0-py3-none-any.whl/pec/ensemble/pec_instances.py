from .pec import _ProgressiveEnsembleClustering


class I_PecK(_ProgressiveEnsembleClustering):
    """Inertia Based Progressive Ensemble Kmeans


    Parameters

    n_clusters : int, default=2.
        The number of clusters to form as well as the number of centroids to generate.

    n_runs : int, default=4
        The number of parallel runs to execute.

    random_state : int or None, default=None
        Determines random number generation for centroid initialization. Use
        an int to make the randomness deterministic.

    observer : ProgressionObserver instance or None, default=None.
        Set the progression observer that rceive the partial results.

    Attributes

    lastResult : PartialResult instance.
        the last generated result (i.e. the result produced at early termination, or a final ternination.
    """

    def __init__(self, data, n_clusters=2, n_runs=4, random_state=None,
                 observer=None, id=None, verbose=False):
        super().__init__(data, n_clusters=n_clusters, n_runs=n_runs,
                         alg="k-means", decision="inertia", random_state=random_state, id=id,
                         observer=observer, verbose=verbose)


class I_PecKPP(_ProgressiveEnsembleClustering):
    """Inertia Based Progressive Ensemble Kmeans++


        Parameters

        n_clusters : int, default=2.
            The number of clusters to form as well as the number of centroids to generate.

        n_runs : int, default=4
            The number of parallel runs to execute.

        random_state : int or None, default=None
            Determines random number generation for centroid initialization. Use
            an int to make the randomness deterministic.

        observer : ProgressionObserver instance or None, default=None.
            Set the progression observer that rceive the partial results.

        Attributes

        lastResult : PartialResult instance.
            the last generated result (i.e. the result produced at early termination, or a final ternination.
        """

    def __init__(self, data, n_clusters=2, n_runs=4, random_state=None,
                 observer=None, id=None, verbose=False):
        super().__init__(data, n_clusters=n_clusters, n_runs=n_runs,
                         alg="k-means++", decision="inertia", random_state=random_state, id=id,
                         observer=observer, verbose=verbose)


'''
class HGPA_PecK(_ProgressiveEnsembleClustering):
    """ HGPA Based Progressive Ensemble Kmeans """

    def __init__(self, data, n_clusters=2, n_runs=4, random_state=None,
                 observer=None, id=None, verbose=False):
        super().__init__(data, n_clusters=n_clusters, n_runs=n_runs,
                         alg="k-means", decision="hgpa", random_state=random_state, id=id,
                         observer=observer, verbose=verbose)


class HGPA_PecKPP(_ProgressiveEnsembleClustering):
    """ HGPA Based Progressive Ensemble Kmeans++ """

    def __init__(self, data, n_clusters=2, n_runs=4, random_state=None,
                 observer=None, id=None, verbose=False):
        super().__init__(data, n_clusters=n_clusters, n_runs=n_runs,
                         alg="k-means++", decision="hgpa", random_state=random_state, id=id,
                         observer=observer, verbose=verbose)


class MCLA_PecK(_ProgressiveEnsembleClustering):
    """ MCLA Based Progressive Ensemble Kmeans """

    def __init__(self, data, n_clusters=2, n_runs=4, random_state=None,
                 observer=None, id=None, verbose=False):
        super().__init__(data, n_clusters=n_clusters, n_runs=n_runs,
                         alg="k-means", decision="mcla", random_state=random_state, id=id,
                         observer=observer, verbose=verbose)


class MCLA_PecKPP(_ProgressiveEnsembleClustering):
    """ MCLA Based Progressive Ensemble Kmeans """

    def __init__(self, data, n_clusters=2, n_runs=4, random_state=None,
                 observer=None, id=None, verbose=False):
        super().__init__(data, n_clusters=n_clusters, n_runs=n_runs,
                         alg="k-means++", decision="mcla", random_state=random_state, id=id,
                         observer=observer, verbose=verbose)
'''