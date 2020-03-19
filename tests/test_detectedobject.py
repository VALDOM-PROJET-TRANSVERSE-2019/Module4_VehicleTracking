import unittest
import numpy as np

from tracker.objects.detectedobject import DetectedObject


class TestInit(unittest.TestCase):
    img = np.zeros([1000, 1000, 3], dtype=np.uint8)
    img.fill(255)
    data = {"object": "truck", "proba": 87, "left": 0, "bot": 1000, "right": 100, "top": 0}
    DO = DetectedObject(data, img)

    def test_init(self):
        self.assertEqual(self.DO.frame_size, (1000, 1000))
        self.assertEqual(self.DO.x, self.data['left'])
        self.assertEqual(self.DO.y, self.data['top'])
        self.assertEqual(self.DO.w, self.data['right'] - self.data['left'])
        self.assertEqual(self.DO.h, self.data['bot'] - self.data['top'])


class TestMeanColor(unittest.TestCase):
    img = np.zeros([1000, 1000, 3], dtype=np.uint8)
    img.fill(255)
    data = {"object": "truck", "proba": 87, "left": 0, "bot": 1000, "right": 100, "top": 0}
    DO = DetectedObject(data, img)

    def test_mean_colors(self):
        self.assertEqual(self.DO.set_mean_color(self.img), (1, 1, 1))
        self.img[:, :, :] = [255, 0, 0]
        self.assertEqual(self.DO.set_mean_color(self.img), (1, 0, 0))
        self.img[:, :, :] = [255, 255, 0]
        self.assertEqual(self.DO.set_mean_color(self.img), (1, 1, 0))
        self.img[:500, :, :] = [255, 127, 2]
        self.img[500:, :, :] = [0, 255, 255]
        self.assertEqual(self.DO.set_mean_color(self.img), ((255 * 500 + 0 * 500) / 1000 / 255,
                                                            (127 * 500 + 255 * 500) / 1000 / 255,
                                                            (2 * 500 + 255 * 500) / 1000 / 255))

class TestGetDistanceFrom(unittest.TestCase):
    def test_get_distance_from(self):
        pass


if __name__ == '__main__':
    unittest.main()
