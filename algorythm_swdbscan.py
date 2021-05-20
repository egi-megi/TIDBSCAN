import numpy as np
import math
import copy

from algorythm_tidbscan import Point, algorythm_tidbscan, read_database, distance_fun_euclides, find_ref_point, sort_fun, distance_from_ref_point, \
    point_to_check, find_border_for_checked_point, rangeQuery


class Cell:
    def __init__(self, id, min, max):
        self.id = id
        self.min_coordinates = min
        self.max_coordinates = max
        self.number_of_points = 0
        self.visited = 0



def make_initial_cells():
    initial_cells_list = []
    min_coor = []
    max_coor = []
    cell = Cell(0, min_coor, max_coor)
    initial_cells_list.append(cell)
    return initial_cells_list



def compute_min_max(data, displacement, degree_of_root, n):
    max_coor = []
    min_coor = []
    displacement_value = 0
    if displacement == 1:
        displacement_value = int((math.pow(n, 1/degree_of_root))/2)
    for i in range(0, len(data[0].cooridantes)):
        max_coor[i] = data[0].cooridantes[i]
        min_coor[i] = data[0].cooridantes[i]
    for j in range(0, len(data)):
        for k in range(0, len(data[0].cooridantes)):
            if data[j].cooridantes[k] > max_coor[k]:
                max_coor[k] = data[j].cooridantes[k]
            if data[j].cooridantes[k] < min_coor[k]:
                min_coor[k] = data[j].cooridantes[k]
    for i in range(0, len(min_coor)):
        min_coor[i] = min_coor[i] + displacement_value
        max_coor[i] = max_coor[i] + displacement_value
    return min_coor, max_coor


def divide_grid(data, displacement):
    n = len(data)
    degree_of_root = 2 * data[0].cooridantes
    number_of_cells = math.pow(n, 1/2)
    number_to_division = int(math.pow(n, 1/degree_of_root))
    range_division = []
    min_coor, max_coor = compute_min_max(data, displacement, degree_of_root, n)
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


def put_point_into_cell(data, displacement):
    cells_list = divide_grid(data, displacement)
    for point in data:
        for cell in cells_list:
            is_in_cell = is_point_on_cell(cell,point)
            if is_in_cell:
                point.cell_number = cell.id
                cell.points.append(point)
                cell.number_of_points = cell.number_of_points + 1
    return cells_list


def find_max_number_of_points(cells_list):
    max_points = 0
    list_of_cells_with_max_number_of_cells = []
    for cell in cells_list:
        if cell.number_of_points > max_points:
            max_points = cell.number_of_points
    for cell in cells_list:
        if cell.number_of_points == max_points:
            list_of_cells_with_max_number_of_cells.append(cell)
    return list_of_cells_with_max_number_of_cells, max_points


def grid_clustering(data, minPts, eps, displacement):
    cells_list = put_point_into_cell(data, displacement)
    list_of_cells_with_max_number_of_cells, max_points = find_max_number_of_points(cells_list)
    divider = 5
    threshold = max_points/divider
    #result = []
    for cell in list_of_cells_with_max_number_of_cells:
        algorythm_tidbscan(minPts, eps, cell.points)
        cell.visited = 1
    for i in range(1, divider + 1):
        eps = eps + 0.1 * eps
        min_range = max_points - i * threshold
        max_range = max_points - (i - 1) * threshold
        for cell in cells_list:
            if cell.visited == 0 and (cell.number_of_points >= min_range and cell.number_of_points < max_range):
                algorythm_tidbscan(minPts, eps, cell.points)
    return data


def get_matrix_M(max_cluster_label_1, max_cluster_label_2, dataBase_1, dataBase_2):
    list_1 = []
    for i in range(0, len(max_cluster_label_1 + 1)):
        list_2 = []
        for j in range(0, len(max_cluster_label_2 + 1)):
            matrix_M[max_cluster_label_1 + 1, max_cluster_label_2 + 1] = list
    for i in range(0, len(dataBase_1)):
        for j in range(0, len(dataBase_2)):
            if dataBase_1[i].id == dataBase_2[j].id:
                matrix_M[dataBase_1[i].cell_number, dataBase_2[j].cell_number].append(dataBase_1[i])
                break
    return matrix_M


def algorythm_swdbscan(minPts, eps, data):
    max_cluster_label_1 = -1
    max_cluster_label_2 = -1
    dataBase_1 = read_database(data)
    dataBase_2 = dataBase_1.copy()
    grid_clustering(dataBase_1, minPts, eps, 0)
    grid_clustering(dataBase_2, minPts, eps, 1)
    for i in range(0, len(dataBase_1)):
        if dataBase_1[i].label > max_cluster_label_1:
            max_cluster_label_1 = dataBase_1[i].label
        if dataBase_2[i].label > max_cluster_label_2:
            max_cluster_label_2 = dataBase_2[i].label
    matrix_M = get_matrix_M(max_cluster_label_1, max_cluster_label_2, dataBase_1, dataBase_2)
    clusters_matrix = np.empty((2, max_cluster_label_2 + 1, 0), dtype=np.int32)
    for k in range(0, max_cluster_label_2 + 1):
        for m in range(0, max_cluster_label_1):
            if matrix_M[m, k] < minPts:
                noise = noise + matrix_M[m, k]
            else:
                group = group + matrix_M[m, k]
        clusters_matrix[0, k] = group
        clusters_matrix[1, k] = noise


    return data


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