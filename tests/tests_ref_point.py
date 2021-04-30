import unittest
import numpy as np

from algorythm_tidbscan import Point, read_database, find_ref_point, distance_from_ref_point, distance_fun_euclides, \
    point_to_check, find_border_for_checked_point, rangeQuery


class RefPointTestCase(unittest.TestCase):
    def setUp(self):
        self.dataArray1 = np.array([[0,0,0], [18,18,21], [4,11,9], [22,0,25], [23,1,29], [24,2,26], [5,8,10],
                                    [20,19,18], [10,15,15], [3,13,11], [19,20,19], [21, 19, 20]])
        self.data1 = read_database(self.dataArray1)
        self.data_base_sort_with_ref_point_1 = distance_from_ref_point(self.data1)
        self.dataArray2 = np.array(
            [[30, 30, 30], [18, 18, 21], [4, 11, 9], [22, 0, 25], [23, 1, 29], [24, 2, 26], [5, 8, 10], [20, 19, 18],
             [10, 15, 15], [3, 13, 11], [19, 20, 19], [21, 19, 20]])
        self.data2 = read_database(self.dataArray2)
        self.minPts = 3
        self.eps = 4

    def test_ref_point_distance_euclides(self):
        self.point_1 = Point([0, 0, 0], 0)
        self.point_2 = Point([18, 18, 21], 1)
        self.distance_euclides = distance_fun_euclides(self.point_1, self.point_2)
        self.assertEqual(self.distance_euclides, 33.0)

    def test_ref_point_like_noise_point(self):
        self.ref_point = find_ref_point(self.data1)
        self.assertTrue((self.ref_point.coordinates == [0, 0, 0]).all())

    def test_ref_point_different_than_noise_point(self):
        self.ref_point = find_ref_point(self.data2)
        self.assertTrue((self.ref_point.coordinates == [3, 0, 9]).all())

    def test_ref_point_distance_sorted(self):
        self.index_in_sorted_database = []
        for i in range(0, len(self.data1)):
            self.index_in_sorted_database.append(self.data_base_sort_with_ref_point_1[i].id)
        self.assertTrue((self.index_in_sorted_database == [0, 6, 2, 9, 8, 7, 1, 3, 10, 11, 5, 4]))

    def test_ref_point_find_point_index(self):
        self.point = Point([18, 18, 21], 1)
        self.index = point_to_check(self.data_base_sort_with_ref_point_1, self.point)
        self.assertEqual(self.index, 6)

    def test_ref_point_find_point_border_point(self):
        self.point = Point([18, 18, 21], 1)
        self.index = point_to_check(self.data_base_sort_with_ref_point_1, self.point)
        self.border_of_indexes = find_border_for_checked_point(self.data_base_sort_with_ref_point_1, self.eps, self.index)
        self.assertEqual(self.border_of_indexes[0], 5)
        self.assertEqual(self.border_of_indexes[1], 10)

    def test_ref_point_find_neighbours(self):
        self.point = Point([18, 18, 21], 1)
        self.index = point_to_check(self.data_base_sort_with_ref_point_1, self.point)
        self.border_of_indexes = find_border_for_checked_point(self.data_base_sort_with_ref_point_1, self.eps, self.index)
        self.neighbours = rangeQuery(self.point, self.eps, self.data_base_sort_with_ref_point_1)
        self.assertEqual(self.neighbours[0].id, 7)
        self.assertEqual(self.neighbours[1].id, 10)
        self.assertEqual(self.neighbours[2].id, 11)
