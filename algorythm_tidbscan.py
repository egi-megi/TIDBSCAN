# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from sklearn.cluster import DBSCAN
import numpy as np
import math


class Point:
    def __init__(self, c, id):
        self.coordinates = c
        self.id = id
        self.label = ["UNDEFINED", "UNDEFINED", "UNDEFINED"]


# X = np.array([[18, 18, 21], [4, 11, 9], [0, 0, 0], [22, 0, 25], [23, 1, 29], [24, 2, 26], [10, 15, 15], [5, 8, 10],
#               [20, 19, 18], [3, 13, 11], [19, 20, 19], [21, 19, 20]])
X = np.array([[22, 0], [23, 1], [24, 2], [1, 13], [4, 11], [6, 8], [3, 7], [20, 19],
                                [18, 18], [19, 20], [21, 19], [15, 5], [16, 16], [0, 9], [1, 4], [19, 18],
                                [20, 17], [18, 18], [24, 0]])
clustering = DBSCAN(eps=4, min_samples=3).fit(X)
print(clustering.labels_)
#
print(clustering)


def printResult(dataBase):
    for point in dataBase:
        print(f'Point {point.id} is in group {point.label[1]}\n')


def read_database(data):
    pointsList = []
    id = 0
    for cooridantes in data:
        point = Point(cooridantes, id)
        pointsList.append(point)
        id = id + 1
    return pointsList


def distance_fun_euclides(point_1, point_2):
    distance = 0
    for i in range(0, len(point_1.coordinates)):
        distance = distance + math.pow(point_1.coordinates[i] - point_2.coordinates[i], 2)
    return math.sqrt(distance)


def find_ref_point(dataBase):
    ref_point_coordinates = dataBase[0].coordinates.copy()
    for i in range(1, len(dataBase)):
        for j in range(0, len(dataBase[0].coordinates)):
            if dataBase[i].coordinates[j] < ref_point_coordinates[j]:
                ref_point_coordinates[j] = dataBase[i].coordinates[j]
    ref_point = Point(ref_point_coordinates, -100)
    return ref_point


def sort_fun(point):
    return point.ref_distance


def distance_from_ref_point(dataBase):
    ref_point = find_ref_point(dataBase)
    for i in range(0, len(dataBase)):
        dataBase[i].ref_distance = distance_fun_euclides(dataBase[i], ref_point)
    data_base_sorted_ref_point = sorted(dataBase, key=sort_fun)
    # for i in range(0, len(ref_point.coordinates)):
    #     print(f'Ref point coorinate {i}: {ref_point.coordinates[i]}')
    return data_base_sorted_ref_point


def point_to_check(sorted_data_base_with_ref_point, point):
    for index, item in enumerate(sorted_data_base_with_ref_point):
        if item.id == point.id:
            break
    else:
        index = -1
    # print(f'Index: {index}')
    return index


def find_border_for_checked_point(sorted_data_base_with_ref_point, eps, point_index):
    earlier_distance = 0
    later_distance = 0
    earlier_index = point_index - 1
    later_index = point_index + 1
    while earlier_index >= 0 and earlier_distance <= eps:
        earlier_distance = sorted_data_base_with_ref_point[point_index].ref_distance - sorted_data_base_with_ref_point[
            earlier_index].ref_distance
        if earlier_distance <= eps:
            earlier_index = earlier_index - 1
    while later_index < len(sorted_data_base_with_ref_point) and later_distance <= eps:
        later_distance = sorted_data_base_with_ref_point[later_index].ref_distance - sorted_data_base_with_ref_point[
            point_index].ref_distance
        if later_distance <= eps:
            later_index = later_index + 1
    return earlier_index + 1, later_index - 1


def rangeQuery(seedPoint, eps, sorted_data_base_with_ref_point):
    neighbours = []
    point_index_in_sorted_database = point_to_check(sorted_data_base_with_ref_point, seedPoint)
    border_of_indexes = find_border_for_checked_point(sorted_data_base_with_ref_point, eps,
                                                      point_index_in_sorted_database)

    for index in range(border_of_indexes[0], border_of_indexes[1] + 1):
        if sorted_data_base_with_ref_point[index].id != seedPoint.id:
            if distance_fun_euclides(sorted_data_base_with_ref_point[index], seedPoint) <= eps:
                neighbours.append(sorted_data_base_with_ref_point[index])
    return neighbours

def algorythm_tidbscan(minPts, eps, data, label_number):
    dataBase = read_database(data)
    algorythm_tidbscan_wo_read(minPts, eps, dataBase, label_number,0)
    return dataBase


def algorythm_tidbscan_wo_read(minPts, eps, dataBase, label_number, min_cluster_id):
    clusterId = min_cluster_id
    data_base_sort_with_ref_point = distance_from_ref_point(dataBase)
    # print(f'data_base_sort_with_ref_point[0]: , {data_base_sort_with_ref_point[0].id}')
    # print(f'data_base[0]: , {dataBase[0].id}')

    for point in dataBase:
        if point.label[label_number] != "UNDEFINED":
            continue
        neighbors = rangeQuery(point, eps, data_base_sort_with_ref_point)
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
                neighborsForSeedPoint = rangeQuery(seedPoint, eps, data_base_sort_with_ref_point)
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
    printResult(dataBase)
    return dataBase, clusterId


def print_hi(name):

    print(f'Hi, {name}')

    dataArray = np.array([[18, 18, 21], [4, 11, 9], [0, 0, 0], [22, 0, 25],
                          [23, 1, 29], [24, 2, 26], [10, 15, 15], [5, 8, 10],
                          [20, 19, 18], [3, 13, 11], [19, 20, 19], [21, 19, 20]])
    algorythm_tidbscan(3, 4, dataArray, 1)


if __name__ == '__main__':
    print_hi('PyCharm')


