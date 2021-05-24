import numpy as np
import math
import copy
from sklearn.cluster import DBSCAN

from algorythm_tidbscan import Point, printResult, read_database, distance_fun_euclides, \
    point_to_check, find_border_for_checked_point


def sort_fun(distance_list):
    return distance_list[0]


def compute_euclides_distance_for_all_points(data):
    i = 0
    while i < len(data) - 1:
        for j in range(i + 1, len(data)):
            distance = distance_fun_euclides(data[i], data[j])
            list_point = [distance, data[j]]
            data[i].distances_to_all_points.append(list_point)
            list_point = [distance, data[i]]
            data[j].distances_to_all_points.append(list_point)
        i = i + 1
    for point in data:
        sorted(point.distances_to_all_points, key=sort_fun)


def rangeQuery(seedPoint, eps, data):
    neighbours = []
    for item in seedPoint.distances_to_all_points:
        if item[0] <= eps:
            neighbours.append(item[1])
    return neighbours


def algorythm_dbscan(minPts, eps, data, label_number):
    dataBase = read_database(data)
    algorythm_dbscan_without_read(minPts, eps, dataBase, label_number, 0)
    return dataBase


def algorythm_dbscan_without_read(minPts, eps, dataBase, label_number, min_cluster_id):
    clusterId = min_cluster_id
    compute_euclides_distance_for_all_points(dataBase)

    for point in dataBase:
        if point.label[label_number] != "UNDEFINED":
            continue
        neighbors = rangeQuery(point, eps, dataBase)
        if len(neighbors) < minPts - 1:
            point.label[label_number] = -1
            continue
        if len(neighbors) >= minPts - 1:
            point.label[label_number] = clusterId
            seedSet = neighbors
        while seedSet:
            seedPoint = seedSet.pop()
            if seedPoint.label[label_number] == -1:
                seedPoint.label[label_number] = clusterId
                continue
            if seedPoint.label[label_number] == "UNDEFINED":
                neighborsForSeedPoint = rangeQuery(seedPoint, eps, dataBase)
                if len(neighborsForSeedPoint) < minPts - 1:
                    seedPoint.label[label_number] = clusterId
                    continue
                if len(neighborsForSeedPoint) >= minPts - 1:
                    seedPoint.label[label_number] = clusterId
                    seed = seedSet + neighborsForSeedPoint
                    seedSet = seed
                    continue
                continue
        clusterId += 1
    # printResult(dataBase)
    return dataBase, clusterId

def print_hi(name):

    print(f'Hi, {name}')

    dataArray = np.array([[18, 18, 21], [4, 11, 9], [0, 0, 0], [22, 0, 25],
                          [23, 1, 29], [24, 2, 26], [10, 15, 15], [5, 8, 10],
                          [20, 19, 18], [3, 13, 11], [19, 20, 19], [21, 19, 20]])

    dataArray2 = np.array([[22, 0], [23, 1], [24, 2], [1, 13], [4, 11], [6, 8], [3, 7], [20, 19],
                                [18, 18], [19, 20], [21, 19], [15, 5], [16, 16], [0, 9], [1, 4], [19, 18],
                                [20, 17], [18, 18], [24, 0]])
    #dataArray22 = dataArray2.reshape(1, -1)
    algorythm_dbscan(3, 4, dataArray2, 1)
    #algorythm_dbscan(3, 4, dataArray2, 1)
    a = int(math.pow(90, 1/4))
    print(f'a: {a}')


if __name__ == '__main__':
    print_hi('PyCharm')