"""
Testing Module for class object DetectedObject
"""
import unittest
import numpy as np

from tracker.objects.detectedobject import DetectedObject


class TestDetectedObject(unittest.TestCase):
    """
    Test functions of DetectedObject
    """

    def setUp(self):
        self.img = np.zeros([1000, 1000, 3], dtype=np.uint8)
        self.img.fill(255)

        self.white_img = np.zeros([1000, 1000, 3], dtype=np.uint8)
        self.white_img.fill(255)

        self.do1_data = {"object": "truck", "proba": 87, "left": 0, "bot": 1000, "right": 100, "top": 0}
        self.do1 = DetectedObject(self.do1_data, self.img)
        self.do2_data = {"object": "truck", "proba": 87, "left": 100, "bot": 400, "right": 200, "top": 300}
        self.do2 = DetectedObject(self.do2_data, self.white_img)

    def test_init(self):
        """
        Test assignment function of __init__
        :return:
        """
        self.assertEqual(self.do1.get_frame_size(), (1000, 1000))
        self.assertEqual(self.do1.get_coordinate()[0], self.do1_data['left'])
        self.assertEqual(self.do1.get_coordinate()[1], self.do1_data['top'])
        self.assertEqual(self.do1.get_coordinate()[2], self.do1_data['right'] - self.do1_data['left'])
        self.assertEqual(self.do1.get_coordinate()[3], self.do1_data['bot'] - self.do1_data['top'])

    def test_mean_colors(self):
        """
        Test mean color function
        :return:
        """
        self.assertEqual(self.do1.get_mean_color(self.img), (1, 1, 1))
        self.img[:, :, :] = [255, 0, 0]
        self.assertEqual(self.do1.get_mean_color(self.img), (1, 0, 0))
        self.img[:, :, :] = [255, 255, 0]
        self.assertEqual(self.do1.get_mean_color(self.img), (1, 1, 0))
        self.img[:500, :, :] = [255, 127, 2]
        self.img[500:, :, :] = [0, 255, 255]
        self.assertEqual(self.do1.get_mean_color(self.img), ((255 * 500 + 0 * 500) / 1000 / 255,
                                                             (127 * 500 + 255 * 500) / 1000 / 255,
                                                             (2 * 500 + 255 * 500) / 1000 / 255))

    def test_get_center(self):
        """
        Test get center function
        :return:
        """
        self.assertEqual(self.do1.get_center(), [50, 500])
        self.assertEqual(self.do2.get_center(), [150.0, 350.0])

    def test_get_distance_from(self):
        """
        Test get_distance_from function
        :return:
        """
        distance_1 = self.do1.get_distance_from(self.do2)
        distance_2 = self.do1.get_distance_from(self.do1)
        distance_3 = self.do2.get_distance_from(self.do2)

        self.assertGreaterEqual(distance_1, 0)
        self.assertEqual(distance_2, distance_3, 0)

    def test_get_feature_array(self):
        """
        Test get_feature_array function
        :return:
        """
        feature_array = self.do2.get_feature_array()
        supposed_feature_array = np.array([0.1, 0.3, 0.1, 0.1, 1, 1, 1])
        self.assertEqual(feature_array.tolist(), supposed_feature_array.tolist())


if __name__ == '__main__':
    unittest.main()
