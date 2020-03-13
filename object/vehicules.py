# coding:utf8

"""
Description :
Class for the tracked vehicule.
"""
import cv2
import numpy as np


class Vehicule(object):
    def __init__(self, id, bounding_box, frame):
        self.bounding_box = bounding_box
        self.x, self.y, self.w, self.h = bounding_box
        self.direction = None
        self.updated = False
        self.trajectory = [self.center]

        self.__init_tracker(bounding_box, frame)
        self.__set_id(id)
        self.__set_center(bounding_box)

    def get_id(self):
        return self.__id

    def __set_direction(self):
        self.direction = np.array(self.trajectory[-1]) - np.array(self.trajectory[-2])

    def __set_center(self, bounding_box):
        x, y, w, h = bounding_box
        xc = (2 * x + w) / 2
        yc = (2 * y + h) / 2
        self.center = np.array([np.float32(xc), np.float32(yc)], np.float32)

    def __set_id(self, id):
        self.__id = id

    def __init_tracker(self, bounding_box, frame):
        x, y, w, h = bounding_box
        self.tracker = cv2.TrackerMedianFlow_create()
        self.tracker.init(frame, (x, y, w, h))

    def update(self, frame):
        self.updated = True
        self.tracker.update(frame)
        ok, new_box = self.tracker.update(frame)
        if ok:
            x, y, w, h = int(new_box[0]), int(new_box[1]), int(new_box[2]), int(new_box[3])
            self.__set_center((x, y, w, h))
            self.bounding_box = (x, y, w, h)
            self.x, self.y, self.w, self.h = self.bounding_box
            self.trajectory.append(self.center)
            self.__set_direction()

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(frame, "Vehicle", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, str(self.__id), (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.polylines(frame, [np.int32(self.trajectory)], 0, (0, 0, 255))
