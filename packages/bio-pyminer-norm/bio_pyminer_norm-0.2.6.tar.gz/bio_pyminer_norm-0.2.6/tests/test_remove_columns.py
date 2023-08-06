import unittest

from scripts.remove_columns import remove_columns


class TestDownsample(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_remove_columns(self):
        #rm_cols = ['Rm_1', 'Rm_2', 'Rm_3', 'Rm_4', 'Rm_5']
        expected_cols = ['gene', 'Keep_1', 'Keep_2', 'Keep_3', 'Keep_4']
        a = remove_columns('test_files/test_rm.txt', "test_files/rm_cols.txt")
        print(a[0])
        for idx, val in enumerate(a[0]):
            self.assertEqual(val, expected_cols[idx])
