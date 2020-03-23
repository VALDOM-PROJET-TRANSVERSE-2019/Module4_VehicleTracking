"""
Testing Module for function Numerical
"""
import unittest

from tracker.track import numerical_sort


class Tests(unittest.TestCase):
    """
    Tests de la fonction numerial sort
    """

    def test_numerical_sort(self):
        """
        tests numerical sort sorting capabilities
        :return:
        """
        names_to_sort = ['image02', 'image01', 'image10', 'image100',
                         'image1001', 'image001002', 'image001000']
        expected_sort = ['image01', 'image02', 'image10', 'image100',
                         'image001000', 'image1001', 'image001002']
        names_sorted = sorted([i for i in names_to_sort], key=numerical_sort)

        self.assertEqual(names_sorted, expected_sort)


if __name__ == '__main__':
    unittest.main()
