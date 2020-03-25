"""
Description :
Class for the tracked vehicle.
"""

import numpy as np
from PIL import ImageDraw

from tracker.objects import DetectedObject


class Vehicle(DetectedObject):
    """
    A tracked vehicle, defined by an unique id and from a DetectedObject
    """

    def __init__(self, do, frame, identifier):
        DetectedObject.__init__(
            self, do.retrieve_bounding_box_coordinate(), frame)
        self.__id = identifier
        self.__previous_visible = True
        self.__visible = True
        self.previous_pos = [[self.get_x(), self.get_y()]]
        self.__prob_x = self.get_x()
        self.__prob_y = self.get_y()
        self.__speed = [0, 0]
        self.update_prob_position()
        self.__counter = 0

    def get_feature_array(self):
        """
        Get feature vector of the vehicle
        :return: array (x,y,w,h,r,g,b)
        """
        x = self.__prob_x / self.get_frame_size()[0]
        y = self.__prob_y / self.get_frame_size()[1]
        w = self.get_w() / self.get_frame_size()[0]
        h = self.get_h() / self.get_frame_size()[1]
        r = self.get_mean_colors()[0]
        g = self.get_mean_colors()[1]
        b = self.get_mean_colors()[2]
        return np.array([x, y, w, h, r, g, b])

    def draw(self, frame):
        """
         Draw rectangle and text on the image
        :param frame: array, frame
        :return:
        """
        draw = ImageDraw.Draw(frame)
        draw.rectangle([(self.get_x(), self.get_y()),
                        (self.get_x() + self.get_w(),
                         self.get_y() + self.get_h())],
                       outline=(0, 255, 0), width=2)
        draw.text([self.get_x(), self.get_y() - 20], "Vehicle", (0, 255, 0))
        draw.text([self.get_x(), self.get_y() - 40], str(self.__id), (0, 255, 0))

    def draw_prob(self, frame):
        """
         Draw rectangle and text on the image
        :param frame: array, frame
        :return:
        """
        draw = ImageDraw.Draw(frame)
        draw.rectangle([(self.get_prob_x(), self.get_prob_y()),
                        (self.get_prob_x() + self.get_w(),
                         self.get_prob_y() + self.get_h())],
                       outline=(255, 0, 255), width=2)
        draw.text([self.get_prob_x(), self.get_prob_y() - 20], "Vehicle", (255, 0, 255))
        draw.text([self.get_prob_x(), self.get_prob_y() - 40], str(self.__id), (255, 0, 255))

    def update_counter(self, visible):
        """
        Update the vehicle counter
        :param visible:
        :return:
        """
        if not self.__previous_visible:
            self.__counter += 1
            self.update_prob_position()
        self.__visible = visible

    def update_visibility(self):
        self.__previous_visible = self.__visible

    def update_vehicle(self, detected_object):
        """
        Update vehicle attributes
        :param detected_object: Object DetectedObject
        :return:
        """
        x, y, w, h = detected_object.get_coordinates()
        self.set_coordinates(x, y, w, h)
        self.__mean_colors = detected_object.get_mean_colors()

        self.previous_pos.append([x, y])
        if len(self.previous_pos) > 10:
            self.previous_pos.pop(0)

        self.__speed = self.compute_speed()

        self.__visible = True

        self.__prob_x = self.get_x()
        self.__prob_y = self.get_y()
        self.update_prob_position()

    def compute_speed(self):
        """
        Compute speed of the detected_object vs the vehicle
        :param detected_object:
        :return: list, (Vx,Vy)
        """
        pos = self.previous_pos
        if len(pos) >= 2:
            speeds = []
            for i in range(1, len(pos), 1):
                speeds.append(np.array(pos[i]) - np.array(pos[i - 1]))
            return list(np.mean(speeds, axis=0) / (self.__counter + 1))
        else:
            return [0, 0]

    def update_prob_position(self):
        """
        Update probable position of the vehicle
        :return:
        """
        self.__prob_x = self.__prob_x + self.__speed[0]
        self.__prob_y = self.__prob_y + self.__speed[1]

    def get_id(self):
        """
        Get vehicle identifier
        :return: id, int
        """
        return self.__id

    def get_visible(self):
        """
        Get visibility of the vehicle
        :return: visible (bool)
        """
        return self.__visible

    def get_previous_visible(self):
        """
        Get previous_visible of the vehicle
        :return: previous_visible (bool)
        """
        return self.__previous_visible

    def get_speed(self):
        """
        Get the speed of the vehicle
        :return: speed (list)
        """
        return self.__speed

    def set_speed(self, speed):
        """
        Set the speed of the vehicle
        """
        self.__speed = speed

    def get_counter(self):
        """
        Get the counter of the vehicle
        :return: counter (int)
        """
        return self.__counter

    def get_prob_x(self):
        """
        Get the prob_x
        :return: prob_x (int)
        """
        return self.__prob_x

    def get_prob_y(self):
        """
        Get the prob_y
        :return: prob_y (int)
        """
        return self.__prob_y
