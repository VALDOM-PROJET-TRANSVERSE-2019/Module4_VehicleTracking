"""
Testing Module for class object DetectedObject
"""
import unittest
import numpy as np

from tracker.objects.detectedobject import DetectedObject


class TestInit(unittest.TestCase):
    """
    Test assignment function of __init__
    """
    img = np.zeros([1000, 1000, 3], dtype=np.uint8)
    img.fill(255)
    data = {"object": "truck", "proba": 87, "left": 0, "bot": 1000, "right": 100, "top": 0}
    DO = DetectedObject(data, img)

    def test_init(self):
        """
        Test assignment function of __init__
        :return:
        """
        self.assertEqual(self.DO.get_frame_size(), (1000, 1000))
        self.assertEqual(self.DO.get_coordinate()[0], self.data['left'])
        self.assertEqual(self.DO.get_coordinate()[1], self.data['top'])
        self.assertEqual(self.DO.get_coordinate()[2], self.data['right'] - self.data['left'])
        self.assertEqual(self.DO.get_coordinate()[3], self.data['bot'] - self.data['top'])


class TestMeanColor(unittest.TestCase):
    """
    Test mean color function
    """
    img = np.zeros([1000, 1000, 3], dtype=np.uint8)
    img.fill(255)
    data = {"object": "truck", "proba": 87, "left": 0, "bot": 1000, "right": 100, "top": 0}
    DO = DetectedObject(data, img)

    def test_mean_colors(self):
        """
        Test mean color function
        :return:
        """
        self.assertEqual(self.DO.get_mean_color(self.img), (1, 1, 1))
        self.img[:, :, :] = [255, 0, 0]
        self.assertEqual(self.DO.get_mean_color(self.img), (1, 0, 0))
        self.img[:, :, :] = [255, 255, 0]
        self.assertEqual(self.DO.get_mean_color(self.img), (1, 1, 0))
        self.img[:500, :, :] = [255, 127, 2]
        self.img[500:, :, :] = [0, 255, 255]
        self.assertEqual(self.DO.get_mean_color(self.img), ((255 * 500 + 0 * 500) / 1000 / 255,
                                                            (127 * 500 + 255 * 500) / 1000 / 255,
                                                            (2 * 500 + 255 * 500) / 1000 / 255))

class TestGetDistanceFrom(unittest.TestCase):
    """
    Test distance function
    """
    def test_get_distance_from(self):
        pass


if __name__ == '__main__':
    unittest.main()
