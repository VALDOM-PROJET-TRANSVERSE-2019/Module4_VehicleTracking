# coding:utf8

"""
Description :
Class for the tracking target.
"""
import cv2
import numpy as np


class Vehicule(object):
    def __init__(self, id, bounding_box, frame):
        self.__id = id
        self.previous_box = None
        self.bounding_box = bounding_box
        self.tracked = None
        self.visible =
        self.direction = 0
        self.center = self._set_center(bounding_box)
        self.trajectory = [self.center]
        self.tracker = self._init_tracker(bounding_box, frame)
        self.number_of_frame = 1


    def __str__(self):
        return str(self.tracker)

    def _set_center(self, bounding_box):
        x, y, w, h = bounding_box
        x = (2 * x + w) / 2
        y = (2 * y + h) / 2
        center = np.array([np.float32(x), np.float32(y)], np.float32)
        return center

    def _init_tracker(self, bounding_box, frame):
        x, y, w, h = bounding_box
        tracker = cv2.TrackerKCF_create()
        tracker.init(frame, (x, y, w, h))
        return tracker

    def update(self, frame):
        self.number_of_frame += 1
        self.tracker.update(frame)
        ok, new_box = self.tracker.update(frame)
        if ok:
            x, y, w, h = int(new_box[0]), int(new_box[1]), int(new_box[2]), int(new_box[3])
            self.center = self._set_center((x, y, w, h))
            self.previous_box = self.bounding_box
            self.bounding_box = (x, y, w, h)
            self.trajectory.append(self.center)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(frame, "vehicle", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, str(self.__id), (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.polylines(frame, [np.int32(self.trajectory)], 0, (0, 0, 255))
