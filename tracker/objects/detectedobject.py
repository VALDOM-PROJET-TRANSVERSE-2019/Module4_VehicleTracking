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
        self.frame_size = (len(frame[0]), len(frame))
        self.x = bounding_box['left']
        self.y = bounding_box['top']
        self.w = bounding_box['right'] - bounding_box['left']
        self.h = bounding_box['bot'] - bounding_box['top']
        self.bounding_box = self.x, self.y, self.w, self.h

        self.center = [self.x + self.w / 2, self.y + self.h / 2]
        self.direction = None
        self.updated = False

        self.mean_colors = self.set_mean_color(frame)

    def set_mean_color(self, frame):
        """
        Get mean color of the frame
        :param frame: array, frame
        :return:
        """
        frame_zone = frame[self.y:self.y + self.h, self.x:self.x + self.w]
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
        :return: array (x,y,w,h,r,g,b)
        """
        x = self.x / self.frame_size[0]
        y = self.y / self.frame_size[1]
        w = self.w / self.frame_size[0]
        h = self.h / self.frame_size[1]
        r = self.mean_colors[0] / 255
        g = self.mean_colors[1] / 255
        b = self.mean_colors[2] / 255
        return np.array([x, y, w, h, r, g, b])
