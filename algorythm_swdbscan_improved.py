import numpy as np
import math
import copy
from sklearn.cluster import DBSCAN

from algorythm_tidbscan import read_database
from algorythm_dbscan import algorythm_dbscan_without_read


class Cell:
    def __init__(self, id, min, max):
        self.id = id
        self.min_coordinates = min
        self.max_coordinates = max
        self.number_of_points = 0
        self.visited = 0
        self.points = []


def print_labels(data):
    for point in data:
        print(point.label[2])


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
    if displacement != 0:
        displacement_value = int((math.pow(n, 1/degree_of_root))/2)
    for coordinate in data[0].coordinates:
        max_coor.append(coordinate)
        min_coor.append(coordinate)
    for j in range(0, len(data)):
        for k in range(0, len(data[0].coordinates)):
            if data[j].coordinates[k] > max_coor[k]:
                max_coor[k] = data[j].coordinates[k]
            if data[j].coordinates[k] < min_coor[k]:
                min_coor[k] = data[j].coordinates[k]
    for i in range(0, len(min_coor)):
        displacement = 0
        if min_coor[i] != 0:
            displacement = min_coor[i]/10
        elif max_coor[i] != 0:
            displacement = max_coor[i]/10
        else:
            displacement = 0.1
        min_coor[i] = min_coor[i] - displacement_value - displacement
        max_coor[i] = max_coor[i] - displacement_value + displacement
    return min_coor, max_coor


def divide_grid(data, displacement):
    n = len(data)
    degree_of_root = 2 * len(data[0].coordinates)
    number_of_cells = math.pow(n, 1/2)
    number_to_division = int(math.pow(n, 1/degree_of_root))
    range_division = []
    min_coor, max_coor = compute_min_max(data, displacement, degree_of_root, n)
    for m in range(0, len(max_coor)):
        range_division.append((max_coor[m] - min_coor[m])/number_to_division)
    cells_list = make_initial_cells()
    for dim in range(0, len(data[0].coordinates)-1):
        new_list = []
        count = 1
        #print("for dim "+str(dim)+" num parts: "+str(len(np.arange(min_coor[dim],max_coor[dim], range_division[dim]).tolist())))
        for cell_begin in (np.arange(min_coor[dim],max_coor[dim], range_division[dim]).tolist()):
            for old_cell in cells_list:
                new_cell=copy.deepcopy(old_cell)
                new_cell.id=count
                count=count+1
                new_cell.min_coordinates.append(cell_begin)
                new_cell.max_coordinates.append(cell_begin+range_division[dim])
                new_list.append(new_cell)
        cells_list=new_list
    return cells_list

def is_point_on_cell(cell,point):
    for dim in range(0, len(point.coordinates)-1):
        if point.coordinates[dim] > cell.max_coordinates[dim] or point.coordinates[dim] < cell.min_coordinates[dim]:
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
    current_cluster_id=0
    label_number = 0
    if displacement != 0:
        label_number = 1
    for cell in list_of_cells_with_max_number_of_cells:
        #_, current_cluster_id = algorythm_tidbscan_without_read(minPts, eps, cell.points, label_number, current_cluster_id)
        _, current_cluster_id = algorythm_dbscan_without_read(minPts, eps, cell.points, label_number,
                                                                current_cluster_id)
        cell.visited = 1
    for i in range(1, divider + 1):
        eps = eps + 0.1 * eps
        min_range = max_points - i * threshold
        max_range = max_points - (i - 1) * threshold
        for cell in cells_list:
            if cell.visited == 0 and (cell.number_of_points >= min_range and cell.number_of_points < max_range):
                #_, current_cluster_id = algorythm_tidbscan_without_read(minPts, eps, cell.points, label_number, current_cluster_id)
                _, current_cluster_id = algorythm_dbscan_without_read(minPts, eps, cell.points, label_number,
                                                                        current_cluster_id)
    return data


def get_matrix_M(max_cluster_label_1, max_cluster_label_2, dataBase):
    matrix_M = []
    for i in range(0, max_cluster_label_1 + 1):
        row = []
        for j in range(0, max_cluster_label_2 + 1):
            list_of_points = []
            row.append(list_of_points)
        matrix_M.append(row)
    for point in dataBase:
        if point.label[0] == "UNDEFINED":
            point.label[0] = -1
        if point.label[1] == "UNDEFINED":
            point.label[1] = -1
        matrix_M[point.label[0]][point.label[1]].append(point)
    return matrix_M


def concatenate_rows_one(matrix_M, max_cluster_label_2, max_cluster_label_1, minPts):
    # for row in matrix_M:
    #     for row2 in matrix_M:
    #         if row != row2:
    #             for col in range(0, max_cluster_label_2 - 1):
    #                 if len(row[col]) >= minPts and len(row2[col]) >= minPts:
    #                     for c in range(0, max_cluster_label_2):
    #                         row[c].extend(row2[c])
    #                     matrix_M.remove(row2)
    #                     print("merging")
    #                     return 1
    for row in range(0, max_cluster_label_1 - 2):
        for row2 in range(1, max_cluster_label_1 - 1):
            for col in range(0, max_cluster_label_2 - 1):
                if len(matrix_M[row][col]) >= 1 and len(matrix_M[row2][col]) >= 1:
                    for c in range(0, max_cluster_label_2):
                        matrix_M[row][c].extend(matrix_M[row2][c])
                    matrix_M.remove(matrix_M[row2])
                    print("merging")
                    return 1
    return 0


def concatenate_rows(matrix_M, max_cluster_label_1, max_cluster_label_2, minPts):
    change = concatenate_rows_one(matrix_M, max_cluster_label_1, max_cluster_label_2,minPts)
    while change > 0:
        change = concatenate_rows_one(matrix_M, max_cluster_label_2, minPts)
    for col in range(0, max_cluster_label_2 - 1):
        if len(matrix_M[max_cluster_label_1 - 1][col]) > 0:
            for row in range(0, max_cluster_label_1 - 1):
                if len(matrix_M[row][col]) > 0:
                    matrix_M[row][col].extend(matrix_M[max_cluster_label_1 - 1][col])
    return matrix_M

# def concatenate_cols_one(matrix_M, max_cluster_label_2, max_cluster_label_1, minPts):
#     # for row in matrix_M:
#     #     for row2 in matrix_M:
#     #         if row != row2:
#     #             for col in range(0, max_cluster_label_2 - 1):
#     #                 if len(row[col]) >= minPts and len(row2[col]) >= minPts:
#     #                     for c in range(0, max_cluster_label_2):
#     #                         row[c].extend(row2[c])
#     #                     matrix_M.remove(row2)
#     #                     print("merging")
#     #                     return 1
#     for col in range(0, max_cluster_label_2 - 2):
#         for col2 in range(1, max_cluster_label_2 - 1):
#             for row in range(0, max_cluster_label_1 - 1):
#                 if len(matrix_M[row][col]) >= 1 and len(matrix_M[row][col2]) >= 1:
#                     for r in range(0, max_cluster_label_1):
#                         matrix_M[r][col].extend(matrix_M[r][col2])
#                     matrix_M.remove(matrix_M[col2])
#                     print("merging")
#                     return 1
#     return 0


# def concatenate_cols(matrix_M, max_cluster_label_1, max_cluster_label_2, minPts):
#     change = concatenate_cols_one(matrix_M, max_cluster_label_1, max_cluster_label_2,minPts)
#     while change > 0:
#         change = concatenate_cols_one(matrix_M, max_cluster_label_2, minPts)
#     for row in range(0, max_cluster_label_1 - 1):
#         if len(matrix_M[row][max_cluster_label_2 - 1]) > 0:
#             for col in range(0, max_cluster_label_2 - 1):
#                 if len(matrix_M[row][col]) > 0:
#                     matrix_M[row][col].extend(matrix_M[row][max_cluster_label_2 - 1])
#     return matrix_M


def compute_ending_clusters(smaller_matrix_M, max_cluster_label_2, minPts):
    for row_num in range(0, len(smaller_matrix_M) - 1):
        row = smaller_matrix_M[row_num]
        for col_num in range(0, len(row) - 1):
       #     amount_of_points = len(smaller_matrix_M[row_num][col_num])
            for point in smaller_matrix_M[row_num][col_num]:
        #        if amount_of_points >= minPts:
                    point.label[2] = row_num
        #        else:
        #            point.label[2] = -1
    for point in smaller_matrix_M[len(smaller_matrix_M) - 1][max_cluster_label_2 - 1]:
        point.label[2] = -1


def algorythm_swdbscan(minPts, eps, data):
    max_cluster_label_1 = -1
    max_cluster_label_2 = -1
    dataBase = read_database(data)
    grid_clustering(dataBase, minPts, eps, 0)
    grid_clustering(dataBase, minPts, eps, 1)
    for p in dataBase:
        if p.label[1] == "UNDEFINED":
            p.label[1] = -1
        if p.label[0] == "UNDEFINED":
            p.label[0] = -1
    for i in range(0, len(dataBase)):
        if dataBase[i].label[0] > max_cluster_label_1:
            max_cluster_label_1 = dataBase[i].label[0]
        if dataBase[i].label[1] > max_cluster_label_2:
            max_cluster_label_2 = dataBase[i].label[1]
    max_cluster_label_1 = max_cluster_label_1 + 1
    max_cluster_label_2 = max_cluster_label_2 + 1
    matrix_M = get_matrix_M(max_cluster_label_1, max_cluster_label_2, dataBase)
    smaller_matrix_M = concatenate_rows(matrix_M, max_cluster_label_1, max_cluster_label_2, minPts)
    #smaller_matrix_M = concatenate_cols(smaller_matrix_M_1, max_cluster_label_1, max_cluster_label_2, minPts)
    compute_ending_clusters(smaller_matrix_M, max_cluster_label_2, minPts)
    for p in dataBase:
        if p.label[2] == "UNDEFINED":
            p.label[2] = -1
    return dataBase


def print_hi(name):

    print(f'Hi, {name}')

    X_2 = np.array([[22, 0], [23, 1], [24, 2], [1, 13], [4, 11], [6, 8], [3, 7], [20, 19],
                                    [18, 18], [19, 20], [21, 19], [15,  5], [0,  9], [1, 4], [19, 18],
                                    [20, 17], [18, 19], [10, 16], [24,  0]])

    X = np.array([[18, 18, 21], [4, 11, 9], [0, 0, 0], [22, 0, 25], [23, 1, 29], [24, 2, 26], [10, 15, 15], [5, 8, 10],
                                 [20, 19, 18], [3, 13, 11], [19, 20, 19], [21, 19, 20]])

    X_1 = np.array([[22, 0], [23, 1], [24, 2], [1, 7], [2, 6], [3, 9], [3, 7], [20, 19],
                                    [18, 18], [19, 20], [21, 19], [15,  5], [0,  9], [1, 4], [19, 18],
                                    [20, 17], [18, 19], [10, 16], [24,  0]])

    #dataArray22 = dataArray2.reshape(1, -1)
    #algorythm_swdbscan(3, 4, dataArray)
    data_to_print = algorythm_swdbscan(4, 4, X_1)
    print_labels(data_to_print)
    a = int(math.pow(90, 1/4))
    print(f'a: {a}')


if __name__ == '__main__':
    print_hi('PyCharm')