# coding:utf8
"""
Description :
Class for the tracked vehicle.
"""

import numpy as np
from PIL import ImageDraw


class Vehicle:
    """
    A tracked vehicle, defined by an unique id and from a DetectedObject
    """

    def __init__(self, detected_object, identifier):
        self.frame_size = detected_object.get_frame_size()
        self.__x, self.__y, self.__w, self.__h = detected_object.get_coordinate()

        self.__id = identifier
        self.visible = True
        self.center = detected_object.get_center()
        self.speed = [0, 0]
        self.update_prob_position()
        self.mean_colors = detected_object.mean_colors
        self.counter = 0

    def get_feature_array(self):
        """
        Get feature vector of the vehicle
        :return: array (x,y,w,h,r,g,b)
        """
        if self.visible:
            x = self.__x / self.frame_size[0]
            y = self.__y / self.frame_size[1]
        else:
            x = self.prob_x / self.frame_size[0]
            y = self.prob_y / self.frame_size[1]
        w = self.__w / self.frame_size[0]
        h = self.__h / self.frame_size[1]
        r = self.mean_colors[0]
        g = self.mean_colors[1]
        b = self.mean_colors[2]
        return np.array([x, y, w, h, r, g, b])

    def draw(self, frame):
        """
         Draw rectangle and text on the image
        :param frame: array, frame
        :return:
        """
        draw = ImageDraw.Draw(frame)
        draw.rectangle([(self.__x, self.__y), (self.__x + self.__w, self.__y + self.__h)],
                       outline=(0, 255, 0), width=2)
        draw.text([self.__x, self.__y - 20], "Vehicle", (0, 255, 0))
        draw.text([self.__x, self.__y - 40], str(self.__id), (0, 255, 0))

    def update_counter(self, visible):
        """
        Update the vehicle counter
        :param visible:
        :return:
        """
        if not self.visible:
            self.counter += 1
            self.update_prob_position()
        self.visible = visible

    def update_vehicle(self, detected_object):
        """
        Update vehicle attributes
        :param detected_object: Object DetectedObject
        :return:
        """
        self.visible = True
        self.speed = self.compute_speed(detected_object)
        self.__x, self.__y, self.__w, self.__h = detected_object.get_coordinate()
        self.center = detected_object.get_center()
        self.mean_colors = detected_object.mean_colors
        self.update_prob_position()

    def compute_speed(self, detected_object):
        """
        Compute speed of the detected_object vs the vehicle
        :param detected_object:
        :return: list, (Vx,Vy)
        """
        return [detected_object.get_x() - self.__x, detected_object.get_y() - self.__y]

    def update_prob_position(self):
        """
        Update probable position of the vehicle
        :return:
        """
        self.prob_x = self.__x + self.speed[0]
        self.prob_y = self.__y + self.speed[1]

    def get_id(self):
        """
        Get vehicle identifier
        :return: id, int
        """
        return self.__id

    def get_coordinate(self):
        """
        Get all coordinates of the vehicle
        :return: x, y, w, h (int, int, int, int)
        """
        return self.__x, self.__y, self.__w, self.__h

    def get_x(self):
        """
        Get x coordinate of the vehicle
        :return: x (int)
        """
        return self.__x

    def get_y(self):
        """
        Get y coordinate of the vehicle
        :return: y (int)
        """
        return self.__y
