import unittest
import numpy as np

from algorythm_tidbscan import read_database, distance_from_ref_point, algorythm_tidbscan
from algorythm_swdbscan import algorythm_swdbscan

class GroupsTestCase(unittest.TestCase):
    def setUp(self):
        self.dataArray = np.array([[22, 0], [23, 1], [24, 2], [1, 13], [4, 11], [6, 8], [3, 7], [20, 19],
                                    [18, 18], [19, 20], [21, 19], [15,  5], [0,  9], [1, 4], [19, 18],
                                    [20, 17], [18, 19], [10, 16], [24,  0]])
        self.data2 = read_database(self.dataArray)
        self.minPts = 3
        self.eps = 4
        self.label_number = 1

    def test_groups_0_sw(self):
        self.data_with_labels = algorythm_swdbscan(self.minPts, self.eps, self.dataArray)
        self.labels = []
        for point in self.data_with_labels:
            self.labels.append(point.label[1])
        print(self.labels)
        self.assertTrue((self.labels == [0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, -1, 2, 2, 1, 1, 1, -1, 0]))


    def test_groups_minPts_4_sw(self):
        self.data_with_labels = algorythm_swdbscan(4, self.eps, self.dataArray)
        self.labels = []
        for point in self.data_with_labels:
            self.labels.append(point.label[1])
        self.assertTrue((self.labels == [0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, -1, 2, 2, 1, 1, 1, -1, 0]))

    def test_groups_minPts_5_sw(self):
        self.data_with_labels = algorythm_swdbscan(5, self.eps, self.dataArray)
        self.labels = []
        for point in self.data_with_labels:
            self.labels.append(point.label[1])
        self.assertTrue((self.labels == [-1, -1, -1, 1, 1, 1, 1, 0, 0, 0, 0, -1, 1, 1, 0, 0, 0, -1, -1]))

    def test_groups_minPts_7_sw(self):
        self.data_with_labels = algorythm_swdbscan(7, self.eps, self.dataArray)
        self.labels = []
        for point in self.data_with_labels:
            self.labels.append(point.label[1])
        self.assertTrue((self.labels == [-1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, -1, -1, -1, 0, 0, 0, -1, -1]))

    # def test_groups_minPts_8_sw(self):
    #     self.data_with_labels = algorythm_swdbscan(8, self.eps, self.dataArray)
    #     self.labels = []
    #     for point in self.data_with_labels:
    #         self.labels.append(point.label[1])
    #     #self.assertTrue((self.labels == [0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, -1, 2, 2, 1, 1, 1, -1, 0]))
    #     self.assertTrue((self.labels == [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]))