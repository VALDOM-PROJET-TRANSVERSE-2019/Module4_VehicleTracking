import cv2
import numpy as np


class DetectedObject(object):
    def __init__(self, bounding_box, frame):
        self.bounding_box = bounding_box
        self.frame = frame
        self.mean_colors = self._set_colors(bounding_box, frame)
        self.center = self._set_center(bounding_box)
        self.probable_velocity = None

    def _set_colors(self, bounding_box, frame):
        img = np.array(frame[bounding_box[1]:bounding_box[1] + bounding_box[3],
                       bounding_box[0]: bounding_box[0] + bounding_box[2]])
        return (np.mean(img[:, :, 0]), np.mean(img[:, :, 1]), np.mean(img[:, :, 2]))

    def _set_center(self, bounding_box):
        x, y, w, h = bounding_box
        x = (2 * x + w) / 2
        y = (2 * y + h) / 2
        center = np.array([np.float32(x), np.float32(y)], np.float32)
        return center


class TrackedVehicule(object):
    def __init__(self, id, DetectedObject, frame):
        self.__id = id
        self.bounding_box = np.array(DetectedObject.bounding_box)
        self.x, self.y, self.w, self.h = DetectedObject.bounding_box
        self.mean_colors = DetectedObject.mean_colors
        self.center = np.array(DetectedObject.center)
        self.velocity = None
        self.futur_center = None
        self.not_visible_counter = 0

        #DEBUG
        self.trajectory = [self.center]

        cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 255, 0), 1)
        cv2.putText(frame, "vehicle", (self.x, self.y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, str(self.__id), (self.x, self.y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.polylines(frame, [np.int32(self.trajectory)], 0, (0, 0, 255))

    def updateCoordinate(self):
        self.x, self.y, self.w, self.h = self.bounding_box

    def updateFound(self, DetectedObject, frame):
        self.velocity = np.array(self.bounding_box) - np.array(DetectedObject.bounding_box)
        self.futur_center = self.center + self.velocity
        self.bounding_box = np.array(DetectedObject.bounding_box)
        self.mean_colors = DetectedObject.mean_colors
        self.center = DetectedObject.center
        self.not_visible_counter = 0


        #DEBUG
        self.updateCoordinate()

        self.trajectory.append(self.center)
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 255, 0), 1)
        cv2.putText(frame, "vehicle", (self.x, self.y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, str(self.__id), (self.x, self.y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.polylines(frame, [np.int32(self.trajectory)], 0, (0, 0, 255))

    def updateNotFound(self, frame):

        self.bounding_box[:2] += np.array(self.velocity)
        self.center += np.array(self.velocity)

        self.not_visible_counter += 1

        #DEBUG
        self.updateCoordinate()
        self.trajectory.append(self.center)
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 255, 0), 1)
        cv2.putText(frame, "vehicle", (self.x, self.y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, str(self.__id), (self.x, self.y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.polylines(frame, [np.int32(self.trajectory)], 0, (0, 0, 255))
