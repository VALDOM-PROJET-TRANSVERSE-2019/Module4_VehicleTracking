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

        self.__mean_colors = self.compute_mean_colors(frame)

    def compute_mean_colors(self, frame):
        """
        Get mean color of the frame
        :param frame: array, frame
        :return:
        """
        frame_zone = frame[self.__y:self.__y +
                           self.__h, self.__x:self.__x + self.__w]
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
        r, g, b = np.array(self.__mean_colors)
        return np.array([x, y, w, h, r, g, b])

    def get_coordinates(self):
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

    def get_h(self):
        """
        Get h coordinate of the DetectedObject
        :return: h (int)
        """
        return self.__h

    def get_w(self):
        """
        Get w coordinate of the DetectedObject
        :return: w (int)
        """
        return self.__w

    def set_coordinates(self, x, y, w, h):
        """
        Set the x, y, w and h coordinates
        """
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h

    def get_frame_size(self):
        """
        Get the size of the frame within the DetectedObject
        :return: frame size (L,H)
        """
        return self.__frame_size

    def get_mean_colors(self):
        """
        Get the mean_colors of a DetectedObject
        :return: mean_colors (tuple)
        """
        return self.__mean_colors

    def retrieve_bounding_box_coordinate(self):
        """
        Return the bounding box with format left, top, right, bot
        :return: bounding_box (dict)
        """
        bounding_box = {
            'left': self.__x,
            'top': self.__y,
            'right': self.__w + self.__x,
            'bot': self.__y+self.__h
        }
        return bounding_box
