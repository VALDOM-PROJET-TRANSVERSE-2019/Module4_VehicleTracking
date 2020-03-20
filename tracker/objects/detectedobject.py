# coding:utf8
"""
Description :
Class for the tracked vehicle.
"""
import numpy as np


class DetectedObject:
    """
    A detected object within a frame defined by a bounding_box
    """

    def __init__(self, bounding_box, frame):
        self.__frame_size = (len(frame[0]), len(frame))
        self.__x = bounding_box['left']
        self.__y = bounding_box['top']
        self.__w = bounding_box['right'] - bounding_box['left']
        self.__h = bounding_box['bot'] - bounding_box['top']

        self.mean_colors = self.get_mean_color(frame)

    def get_center(self):
        return [self.__x + self.__w / 2, self.__y + self.__h / 2]

    def get_mean_color(self, frame):
        """
        Get mean color of the frame
        :param frame: array, frame
        :return:
        """
        frame_zone = frame[self.__y:self.__y + self.__h, self.__x:self.__x + self.__w]
        frame_zone = np.array(frame_zone)
        color_r = np.mean(frame_zone[:, :, 0]) / 255
        color_g = np.mean(frame_zone[:, :, 1]) / 255
        color_b = np.mean(frame_zone[:, :, 2]) / 255
        return color_r, color_g, color_b

    def get_distance_from(self, vehicle):
        """
        Compute the distance of the detectedObject to the vehicle
        :param vehicle: Object Vehicle
        :return: nparray, dist
        """
        do_array = self.get_feature_array()
        dv_array = vehicle.get_feature_array()
        dist = np.linalg.norm(do_array - dv_array)
        return dist

    def get_feature_array(self):
        """
        Get feature vector of the DetectedObject
        :return: array (x, y, w, h, r, g, b)
        """
        x = self.__x / self.__frame_size[0]
        y = self.__y / self.__frame_size[1]
        w = self.__w / self.__frame_size[0]
        h = self.__h / self.__frame_size[1]
        r, g, b = np.array(self.mean_colors) / 255
        return np.array([x, y, w, h, r, g, b])

    def get_coordinate(self):
        """
        Get all coordinates of the DetectedObject
        :return: x, y, w, h (int, int, int, int)
        """
        return self.__x, self.__y, self.__w, self.__h

    def get_x(self):
        """
        Get x coordinate of the DetectedObject
        :return: x (int)
        """
        return self.__x

    def get_y(self):
        """
        Get y coordinate of the DetectedObject
        :return: y (int)
        """
        return self.__y

    def get_frame_size(self):
        """
        Get the size of the frame within the DetectedObject
        :return: frame size (L,H)
        """
        return self.__frame_size
