# coding:utf8
"""
Description :
Class for the tracked vehicle.
"""
import cv2
import numpy as np


class Vehicle:
    """
    A tracked vehicle, defined by an unique id and from a DetectedObject
    """
    def __init__(self, detected_object, id):
        self.frame_size = detected_object.frame_size
        self.x = detected_object.x
        self.y = detected_object.y
        self.w = detected_object.w
        self.h = detected_object.h
        self.bounding_box = self.x, self.y, self.w, self.h

        self.id = id
        self.visible = True
        self.center = detected_object.center
        self.speed = [0, 0]
        self.update_prob_position()
        self.updated = False
        self.mean_colors = detected_object.mean_colors
        self.counter = 0


    def get_mean_color(self, frame):
        """
        Get mean color of the frame
        :param frame: array, frame
        :return:
        """
        frame_zone = frame[self.y:self.y + self.h, self.x:self.x + self.w]
        frame_zone = np.array(frame_zone)
        color_r = np.mean(frame_zone[:, :, 0])
        color_g = np.mean(frame_zone[:, :, 1])
        color_b = np.mean(frame_zone[:, :, 2])
        self.mean_colors = (color_r, color_g, color_b)

    def get_feature_array(self):
        """
        Get feature vector of the vehicle
        :return: array (x,y,w,h,r,g,b)
        """
        if self.visible:
            x = self.x / self.frame_size[0]
            y = self.y / self.frame_size[1]
        else:
            x = self.prob_x / self.frame_size[0]
            y = self.prob_y / self.frame_size[1]
        w = self.w / self.frame_size[0]
        h = self.h / self.frame_size[1]
        r = self.mean_colors[0] / 255
        g = self.mean_colors[1] / 255
        b = self.mean_colors[2] / 255
        return np.array([x, y, w, h, r, g, b])

    def draw(self, frame):
        """
        Draw rectangle and text on the image
        :param frame: array, frame
        :return:
        """
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 255, 0), 1)
        cv2.putText(frame, "Vehicle", (self.x, self.y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, str(self.id), (self.x, self.y - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

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
        self.x = detected_object.x
        self.y = detected_object.y
        self.w = detected_object.w
        self.h = detected_object.h
        self.bounding_box = self.x, self.y, self.w, self.h
        self.center = detected_object.center
        self.mean_colors = detected_object.mean_colors
        self.update_prob_position()

    def compute_speed(self, detected_object):
        """
        Compute speed of the detected_object vs the vehicle
        :param detected_object:
        :return: list, (Vx,Vy)
        """
        return [detected_object.x - self.x, detected_object.y - self.y]

    def update_prob_position(self):
        """
        Update probable position of the vehicle
        :return:
        """
        self.prob_x = self.x + self.speed[0]
        self.prob_y = self.y + self.speed[1]
