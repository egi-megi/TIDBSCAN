# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from sklearn.cluster import DBSCAN
import numpy as np
import math



class Point:

    coordinates = {}

    def __init__(self, c, id):
        self.coordinates = c
        self.id = id
        self.label = "UNDEFINED"

X = np.array([[1, 2], [2, 2], [2, 3], [8, 7], [8, 8], [25, 80]])
clustering = DBSCAN(eps=3, min_samples=2).fit(X)
print(clustering.labels_)

print(clustering)



def printResult(dataBase):
    for point in dataBase:
        print(f'Point {point.id} is in group {point.label}\n')


def rangeQuery(dataBase, seedPoint, eps):
    neighbours = []
    for point in dataBase:
        if point.id != seedPoint.id:
            if distance_fun_euclides(point, seedPoint) <= eps:
                neighbours.append(point)
    return neighbours


def read_database():
    pointsList = []
    X = np.array([[1, 2], [2, 2], [8, 8], [25, 80], [2, 3], [8, 7]])
    id = 0
    for cooridantes in X:
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
    ref_point_coordinates = dataBase[0].coordinates
    for i in range(1, len(dataBase)):
        for j in range(0, len(dataBase[0].coordinates)):
            if dataBase[i].coordinates[j] < ref_point_coordinates[j]:
                ref_point_coordinates[j] = dataBase[i].coordinates[j]
    ref_point = Point(ref_point_coordinates, -1)
    return ref_point


def sort_fun(point):
    return point.ref_distance


def distance_form_ref_point(dataBase):
    ref_point = find_ref_point(dataBase)
    for i in range(0, len(dataBase)):
        dataBase[i].ref_distance = distance_fun_euclides(dataBase[i], ref_point)
    data_base_sorted_ref_point = sorted(dataBase, key=sort_fun)
    for i in ref_point.coordinates:
        print(f'Ref point: {i}')
    return data_base_sorted_ref_point


def point_to_check(data_base_sort_with_ref_point, eps, point):
    for index, item in enumerate(data_base_sort_with_ref_point):
        if item.id == point.id:
            break
    else:
        index = -1
    print(f'Index: {index}')
    return index



def algorythm_tidbscan(minPts, eps):
    clusterId = 0
    dataBase = read_database()
    data_base_sort_with_ref_point = distance_form_ref_point(dataBase)
    point_to_check(data_base_sort_with_ref_point, eps, dataBase[3])

    for point in dataBase:
        if point.label != "UNDEFINED":
            continue
        neighbors = rangeQuery(dataBase, point, eps)
        if len(neighbors) < minPts:
            point.label = "NOISE"
            continue
        if len(neighbors) >= minPts:
            point.label = clusterId
            seedSet = neighbors
        while seedSet:
            seedPoint=seedSet.pop()
            if dataBase[seedPoint.id].label == "NOISE":
                dataBase[seedPoint.id].label = clusterId
                continue
            if dataBase[seedPoint.id].label == "UNDEFINED":
                neighborsForSeedPoint = rangeQuery(dataBase, seedPoint, eps)
                if len(neighborsForSeedPoint) < minPts:
                    dataBase[seedPoint.id].label = clusterId
                    continue
                if len(neighborsForSeedPoint) >= minPts:
                    dataBase[seedPoint.id].label = clusterId
                    seed = seedSet + neighborsForSeedPoint
                    seedSet = seed
                    print("set")
                    for i in seedSet:
                        print(f'Seed: {i.id}')
                    print("end set")
                    continue
                continue
        clusterId += 1
    printResult(dataBase)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
    algorythm_tidbscan(1, 1)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
