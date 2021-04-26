import unittest
import numpy as np

import responses
import requests
from main import Data, Point, read_database, find_ref_point, distance_from_ref_point


class NoiseTestCase(unittest.TestCase):
    def setUp(self):
        self.dataArray = np.array([[1, 2]])
        self.data = Data(self.dataArray)
        self.minPts = 1
        self.eps = 1

    def test_compute_reference_point(self):
        self.dataBase = read_database(self.dataArray)
        self.sorted_database = distance_from_ref_point(self.dataBase)
        #self.assertIsNotNone(self.sorted_database[0])
        self.point = Point([1, 2], 0)
        self.assertEqual(self.sorted_database[0], self.dataBase[0])
