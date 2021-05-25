import unittest
import numpy as np

from algorythm_tidbscan import read_database, distance_from_ref_point, algorythm_tidbscan
from algorythm_swdbscan import algorythm_swdbscan
from algorythm_dbscan import algorythm_dbscan


class GroupsTestCase(unittest.TestCase):
    def setUp(self):
        self.dataArray1 = np.array([[0,0,0], [18,18,21], [4,11,9], [22,0,25], [23,1,29], [24,2,26], [5,8,10],
                                    [20,19,18], [3,13,11], [19,20,19], [21, 19, 20], [10,15,15]])
        self.data1 = read_database(self.dataArray1)
        self.data_base_sort_with_ref_point_1 = distance_from_ref_point(self.data1)
        self.minPts = 3
        self.eps = 4
        self.label_number = 0

    def test_groups_0(self):
        self.data_with_labels = algorythm_tidbscan(self.minPts, self.eps, self.dataArray1, self.label_number)
        #self.data_with_labels = algorythm_dbscan(self.minPts, self.eps, self.dataArray1, self.label_number)
        self.labels = []
        for point in self.data_with_labels:
            self.labels.append(point.label[0])
        print(self.labels)
        self.assertTrue((self.labels == [-1, 0, 1, 2, 2, 2, 1, 0, 1, 0, 0, -1]))

    def test_groups_minPts_4(self):
        self.data_with_labels = algorythm_tidbscan(4, self.eps, self.dataArray1, self.label_number)
        #self.data_with_labels = algorythm_dbscan(4, self.eps, self.dataArray1, self.label_number)
        self.labels = []
        for point in self.data_with_labels:
            self.labels.append(point.label[0])
        self.assertTrue((self.labels == [-1, 0, -1, -1, -1, -1, -1, 0, -1, 0, 0, -1]))

    def test_groups_minPts_2(self):
        self.data_with_labels = algorythm_tidbscan(2, self.eps, self.dataArray1, self.label_number)
        #self.data_with_labels = algorythm_dbscan(2, self.eps, self.dataArray1, self.label_number)
        self.labels = []
        for point in self.data_with_labels:
            self.labels.append(point.label[0])
        self.assertTrue((self.labels == [-1, 0, 1, 2, 2, 2, 1, 0, 1, 0, 0, -1]))

    def test_groups_noise(self):
        self.data_with_labels = algorythm_tidbscan(5, self.eps, self.dataArray1, self.label_number)
        #self.data_with_labels = algorythm_dbscan(5, self.eps, self.dataArray1, self.label_number)
        self.labels = []
        for point in self.data_with_labels:
            self.labels.append(point.label[0])
        self.assertTrue((self.labels == [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]))