import math
import traceback

import numpy as np
import sklearn.metrics as _skmetrics


class ClusteringMetrics:
    @staticmethod
    def _get_clusters(data, labels):
        """
        Returns clusters, centroid, point indexes for each cluster, unique labels
        """
        unique_labels = np.unique(labels)
        clusters_idx = [np.where(labels==l) for l in unique_labels]
        clusters = [data[i] for i in clusters_idx]
        centroids = np.array([np.mean(c, axis=0) for c in clusters], dtype=float)
        return clusters, centroids, clusters_idx, unique_labels

    
    @staticmethod
    def inertia(data, labels):
        """Inertia"""
        result = 0.0

        n = data.shape[0]
        d = data.shape[1]
        unique_labels = np.lib.arraysetops.unique(labels)
        k = unique_labels.shape[0]
        for i in range(k):
            idx = np.argwhere(labels == unique_labels[i]).flatten()
            centroid = np.mean(data[idx], axis=0) #mean point inside the cluster
            #center_idx, _ = pairwise_distances_argmin_min([centroid], data[idx], metric="euclidean") # real point closest to mean_center
            #center = data[idx][center_idx][0]
            result += np.sum(np.square(_skmetrics.pairwise.euclidean_distances(data[idx], [centroid])))

        return result / n

    @staticmethod
    def ARI(labels_a, labels_b):
        """Adjusted Rand Index, see sklearn.metrics.adjusted_rand_score"""
        return _skmetrics.adjusted_rand_score(labels_a, labels_b)

    @staticmethod
    def AMI(labels_a, labels_b):
        """Adjusted Mutual Information, see sklearn.metrics.adjusted_mutual_info_score"""
        return _skmetrics.adjusted_mutual_info_score(labels_a, labels_b)

    @staticmethod
    def calinsky_harabaz(data, labels):
        """Calinski and Harabasz score, see calinski_harabasz_score"""
        return _skmetrics.calinski_harabasz_score(data, labels)

    @staticmethod
    def davies_bouldin_index(data, labels):
        """Davies-Bouldin score, see sklearn.metrics.davies_bouldin_score"""
        return _skmetrics.davies_bouldin_score(data, labels)
    
    @staticmethod
    def dunn_index(data, labels):
        """Dunn index"""
        clusters = []
        for class_name in np.lib.arraysetops.unique(labels):
            idx = np.argwhere(labels == class_name).flatten()
            clusters.append(data[idx])
                
        centroids = [np.mean(cl, axis=0) for cl in clusters]
        centroids_pairwise_distances = _skmetrics.pairwise.euclidean_distances(centroids)

        max_cluster_diameter = 0
        for i in range(len(clusters)):
            cluster = clusters[i]
            centroid = centroids[i]
            distances = _skmetrics.pairwise.euclidean_distances(cluster, [centroid])
            max_cluster_diameter = max(np.mean(distances), max_cluster_diameter)
                
        idx = np.triu_indices(centroids_pairwise_distances.shape[0], 1)
        min_centroids_distance = np.min(centroids_pairwise_distances[idx])   
        result = min_centroids_distance / max_cluster_diameter
        return result

    @staticmethod
    def silhouette(data, labels):
        """Silhouette Coefficient of all samples, see sklearn.metrics.silhouette_score"""
        return _skmetrics.silhouette_score(data, labels)


    @staticmethod
    def simplified_silhouette(data, labels):
        """Simplified Silhouette Coefficient of all samples"""
        n = data.shape[0]
        clusters, centroids, clusters_idx, unique_labels = ClusteringMetrics._get_clusters(data, labels)
        distances = _skmetrics.pairwise.euclidean_distances(data, centroids) #distance of each point to all centroids
        try:
            A = distances[np.arange(n), labels] #distance of each point to its cluster centroid
            distances[np.arange(n), labels] = np.Inf #set to infinte the distance to own centroid
            B = np.min(distances, axis=1) #distance to each point to the other closer centroid (different from its own cluster)
            M = np.maximum(A, B) #max row wise of A and B
            S = np.mean( (B - A) / M )
            return S
        except:
            traceback.print_exc()
            print(n, centroids.shape, distances.shape, labels.shape)
            return 0

    @staticmethod
    def entries_stability(labelsHistory, window=None):
        hist = None

        if window is None:
            if len(labelsHistory) >= 5:
                hist = labelsHistory
        elif window < 2:
            raise RuntimeError(f"Window must me >=2")
        
        else:
            hist = labelsHistory[-window:] # last window elements
        
        
        stability = np.full_like(labelsHistory[0], 0, dtype=float)
        if hist is None:
            return stability
        
        h = len(hist)
        w = [math.log(2 + i) for i in range(h-1)] #log weights
        #w = [math.exp(i) for i in range(h-1)] #exp weights
        for i in range(h-1):
            stability += ( (labelsHistory[h-1] == labelsHistory[i]).astype(float) * w[i] ) / sum(w)  
        return stability


    @staticmethod
    def global_stability(labelsHistory, window=None):
        return np.mean(ClusteringMetrics.entries_stability(labelsHistory, window))