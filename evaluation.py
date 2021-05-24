from sklearn import metrics
import numpy as np


def get_purity_score(class_vector, labels):
    scores = []
    for i in range(len(labels)):
        scores.append(purity_score(class_vector, labels[i]))

    return scores


def purity_score(y_true, y_pred):
    # Source: https://stackoverflow.com/a/51672699
    # compute contingency matrix (also called confusion matrix)
    contingency_matrix = metrics.cluster.contingency_matrix(y_true, y_pred)
    # return purity
    return np.sum(np.amax(contingency_matrix, axis=0)) / np.sum(contingency_matrix)


def get_silhouette_score_xdbscan(X, labels):
    scores = []
    for i in range(len(X)):
        scores.append(metrics.silhouette_score(X[i], labels[i], metric='euclidean'))

    return scores


def get_davies_bouldin_score_xdbscan(X, labels):
    scores = []
    for i in range(len(X)):
        scores.append(metrics.davies_bouldin_score(X[i], labels[i]))

    return scores


def flatten_list_of_results(results):
    labels = []
    X = []
    for j in range(len(results)):
        labels.append([results[j][i].label[1] for i in range(len(results[0]))])
        X.append([results[j][i].coordinates for i in range(len(results[0]))])

    return [X, labels]
