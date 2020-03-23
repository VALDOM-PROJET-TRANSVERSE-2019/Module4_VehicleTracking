"""
Module for testing overlapping function with unittest
"""
import unittest

from tracker import track


class TestOverlap(unittest.TestCase):
    """
    Tests de la fonction overlap
    """
    bb1 = (100, 100, 100, 100)
    bb2 = (100 + 100, 100 + 100, 1000, 1000)
    bb3 = (100 + 50, 100, 100, 100)
    bb4 = (100 + 50, 100, 50, 100)
    bb5 = (100, 100, 50, 50)

    bb6 = (10, 10, 1000, 10)
    bb7 = (30, 30, 10, 10)

    bb8 = (10, 10, 10, 1000)
    bb9 = (30, 30, 10, 10)

    def test_bb_full_overlap(self):
        """
        test full overlap between to boxes
        :return:
        """
        self.assertEqual(1, track.overlap(self.bb1, self.bb1))

    def test_bb_no_overlap(self):
        """
        test no overlap between to boxes
        :return:
        """
        self.assertEqual(0, track.overlap(self.bb1, self.bb2))
        self.assertEqual(0, track.overlap(self.bb2, self.bb1))

    def test_bb_third_overlap(self):
        """
        test 1/3 overlap between to boxes
        :return:
        """
        self.assertEqual(1 / 3, track.overlap(self.bb1, self.bb3))
        self.assertEqual(1 / 3, track.overlap(self.bb3, self.bb1))

    def test_bb_half_overlap(self):
        """
           test half overlap between to boxes
           :return:
        """
        self.assertEqual(1 / 2, track.overlap(self.bb1, self.bb4))
        self.assertEqual(1 / 2, track.overlap(self.bb4, self.bb1))

    def test_bb_quarter_overlap(self):
        """
        test 1/4 overlap between to boxes
        :return:
        """
        self.assertEqual(0.25, track.overlap(self.bb5, self.bb1))
        self.assertEqual(0.25, track.overlap(self.bb1, self.bb5))

    def test_overlap(self):
        """
        test 1/4 overlap between to boxes
        :return:
        """
        self.assertEqual(0.25, track.overlap(self.bb5, self.bb1))
        self.assertEqual(0.25, track.overlap(self.bb1, self.bb5))

    def test_no_overlap_height(self):
        """
        test no overlap because of height
        :return:
        """
        self.assertEqual(0, track.overlap(self.bb6, self.bb7))

    def test_no_overlap_width(self):
        """
        test no overlap because of width
        :return:
        """
        self.assertEqual(0, track.overlap(self.bb8, self.bb9))


if __name__ == '__main__':
    unittest.main()
