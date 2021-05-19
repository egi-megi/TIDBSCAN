import numpy as np
import math
import copy

from algorythm_tidbscan import Point, read_database, distance_fun_euclides, find_ref_point, sort_fun, distance_from_ref_point, \
    point_to_check, find_border_for_checked_point, rangeQuery


class Cell:
    def __init__(self, id, min, max):
        self.id = id
        self.min_coordinates = min
        self.max_coordinates = max
        number_of_points = 0


def make_initial_cells():
    initial_cells_list = []
    min_coor = []
    max_coor = []
    cell = Cell(0, min_coor, max_coor)
    initial_cells_list.append(cell)
    return initial_cells_list



def compute_min_max(data):
    max_coor = []
    min_coor = []
    for i in range(0, len(data[0].cooridantes)):
        max_coor[i] = data[0].cooridantes[i]
        min_coor[i] = data[0].cooridantes[i]
    for j in range(0, len(data)):
        for k in range(0, len(data[0].cooridantes)):
            if data[j].cooridantes[k] > max_coor[k]:
                max_coor[k] = data[j].cooridantes[k]
            if data[j].cooridantes[k] < min_coor[k]:
                min_coor[k] = data[j].cooridantes[k]
    return min_coor, max_coor


def divide_grid(data):
    n = len(data)
    degree_of_root = 2 * data[0].cooridantes
    number_of_cells = math.pow(n, 1/2)
    number_to_division = int(math.pow(n, 1/degree_of_root))
    range_division = []
    min_coor, max_coor = compute_min_max(data)
    for m in range(0, len(max_coor)):
        range_division[m] = (max_coor[m] - min_coor[m])/number_to_division
        #policzyć współrzędne komórek
    cells_list = make_initial_cells()
    for dim in (0, data[0].coordinates):
        new_list = []
        count = 1
        for cell_begin in range(min_coor[dim],max_coor[dim], step=range_division[dim]):
            for old_cell in cells_list:
                new_cell=copy.deepcopy(old_cell)
                new_cell.id=count
                count=count+1
                new_cell.min_coordinates[dim]=cell_begin
                new_cell.max_coordinates[dim]=cell_begin+range_division[dim]
                new_list.append(new_cell)
        cells_list=new_list
    return cells_list

def is_point_on_cell(cell,point):
    for dim in range(0, point.coordinates):
        if point.coordinates[dim] > cell.max_coordinates or point.coordinates[dim] < cell.min_coordinates:
            return False
    return True


def put_point_into_cell(data):
    cells_list = divide_grid(data)
    for point in data:
        for cell in cells_list:
            is_in_cell = is_point_on_cell(cell,point)
            if is_in_cell:
                point.cell_number = cell.id
                cell.points.append(point)
                cell.number_of_points = cell.number_of_points + 1


def algorythm_swdbscan(minPts, eps, data):
    clusterId = 0
    dataBase = read_database(data)
    data_base_sort_with_ref_point = distance_from_ref_point(dataBase)
    # print(f'data_base_sort_with_ref_point[0]: , {data_base_sort_with_ref_point[0].id}')
    # print(f'data_base[0]: , {dataBase[0].id}')

    for point in dataBase:
        if point.label != "UNDEFINED":
            continue
        neighbors = rangeQuery(point, eps, data_base_sort_with_ref_point)
        if len(neighbors) < minPts - 1:
            point.label = -1
            continue
        if len(neighbors) >= minPts - 1:
            point.label = clusterId
            seedSet = neighbors
        while seedSet:
            seedPoint = seedSet.pop()
            if dataBase[seedPoint.id].label == -1:
                dataBase[seedPoint.id].label = clusterId
                continue
            if dataBase[seedPoint.id].label == "UNDEFINED":
                neighborsForSeedPoint = rangeQuery(seedPoint, eps, data_base_sort_with_ref_point)
                if len(neighborsForSeedPoint) < minPts - 1:
                    dataBase[seedPoint.id].label = clusterId
                    continue
                if len(neighborsForSeedPoint) >= minPts - 1:
                    dataBase[seedPoint.id].label = clusterId
                    seed = seedSet + neighborsForSeedPoint
                    seedSet = seed
                    # print("set")
                    # for i in seedSet:
                        # print(f'Seed: {i.id}')
                    # print("end set")
                    continue
                continue
        clusterId += 1

    return dataBase


def print_hi(name):

    print(f'Hi, {name}')

    dataArray = np.array([[18, 18, 21], [4, 11, 9], [0, 0, 0], [22, 0, 25],
                          [23, 1, 29], [24, 2, 26], [10, 15, 15], [5, 8, 10],
                          [20, 19, 18], [3, 13, 11], [19, 20, 19], [21, 19, 20]])
    #algorythm_swdbscan(3, 4, dataArray)
    a = int(math.pow(90, 1/4))
    print(f'a: {a}')


if __name__ == '__main__':
    print_hi('PyCharm')