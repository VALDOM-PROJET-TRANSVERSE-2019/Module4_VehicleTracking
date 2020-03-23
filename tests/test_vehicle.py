"""
Testing Module for class object DetectedObject
"""
import unittest
import numpy as np
from PIL import Image
from tracker.objects.detectedobject import DetectedObject
from tracker.objects.vehicle import Vehicle


class TestVehicle(unittest.TestCase):
    """
    Test functions of Vehicle
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

    def test_constructor(self):
        """
        Test correct initialization from a detectedObject
        :return:
        """
        dv1 = Vehicle(self.do1, 0)

        dv1_coordinates = dv1.get_coordinate()
        do1_coordinates = self.do1.get_coordinate()

        self.assertEqual(dv1_coordinates, do1_coordinates)
        self.assertEqual(dv1.get_id(), 0)
        self.assertEqual(dv1.get_mean_colors(), self.do1.get_mean_colors())
        self.assertEqual(dv1.get_speed(), [0, 0])
        self.assertEqual(dv1.get_visible(), True)
        self.assertEqual(dv1.get_counter(), 0)

    def test_get_feature_array(self):
        """
        Test the get feature_array_function
        :return:
        """
        dv1 = Vehicle(self.do1, 0)
        self.assertEqual(dv1.get_feature_array().tolist(), [0, 0, 0.1, 1, 1, 1, 1])

    def test_draw(self):
        """
        Test the draw function
        :return:
        """
        dv1 = Vehicle(self.do1, 0)
        img_pil = Image.fromarray(self.img)
        dv1.draw(img_pil)
        self.assertEqual(np.asarray(img_pil)[0][0].tolist(), [0, 255, 0])

    def test_update_counter(self):
        """
        Test the update_counter function
        :return:
        """
        dv1 = Vehicle(self.do1, 0)

        dv1.update_counter(False)
        self.assertEqual(dv1.get_counter(), 0)
        dv1.update_counter(False)
        self.assertEqual(dv1.get_counter(), 1)

    def test_compute_speed(self):
        """
        Test the compute speed function
        :return:
        """
        dv1 = Vehicle(self.do1, 0)
        self.assertEqual(dv1.compute_speed(self.do1), [0, 0])
        self.assertEqual(dv1.compute_speed(self.do2), [100, 300])

    def test_update_prob_position(self):
        """
        Test the update_prob_position function
        :return:
        """
        dv1 = Vehicle(self.do1, 0)
        dv1.set_speed([1, 15])
        dv1.update_prob_position()

        self.assertEqual(dv1.prob_x, dv1.get_x() + dv1.get_speed()[0])
        self.assertEqual(dv1.prob_y, dv1.get_y() + dv1.get_speed()[1])

    def test_update_vehicle(self):
        """
        Test the update_vehicle function
        :return:
        """
        dv1 = Vehicle(self.do1, 0)
        dv1.update_vehicle(self.do2)

        dv1_coordinates = dv1.get_coordinate()
        do2_coordinates = self.do2.get_coordinate()
        self.assertEqual(dv1_coordinates, do2_coordinates)
        self.assertEqual(dv1.get_speed(), [100, 300])


if __name__ == '__main__':
    unittest.main()
