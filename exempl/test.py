import unittest
from my_sum import sum
# (elpy-set-project-root "f:/Dev/Src/Rogalik/")
# (message elpy-project-root)

class TestSum(unittest.TestCase):
    def test_list_int(self):
        """
        Test that it can sum a list of integers
        """
        import os
        print("root =", os.getcwd())
        data = [1, 2, 3]
        result = sum(data)
        self.assertEqual(result, 6)

if __name__ == '__main__':
    unittest.main()
