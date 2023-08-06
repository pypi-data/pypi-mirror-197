import unittest

import numpy as np

from scripts.common_functions import flatten_2D_table


class TestDownsample(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        pass

    def test_flatten_2D_table(self):
        dummy_mat = np.array((['a', 'b'], ['c', 'd']), dtype=str)
        dummy_list = dummy_mat.tolist()
        a = flatten_2D_table(dummy_list, '\t')
        self.assertEqual(a, ['a\tb\n', 'c\td\n'])

        dummy_mixed_list = dummy_mat
        dummy_mixed_list[0][1] = 0
        dummy_mixed_list[1][1] = 1
        b = flatten_2D_table(dummy_mixed_list, '\t')
        self.assertEqual(b, ['a\t0\n', 'c\t1\n'])
