import unittest

from SRC.data_loaders import load_game, save_game, save_char, load_char, save_citadel, load_citadel, import_char


class TestSum(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 2)), 5, "Should be 6")

if __name__ == '__main__':
    unittest.main()
