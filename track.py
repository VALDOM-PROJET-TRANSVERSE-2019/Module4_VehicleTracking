import sys
import copy
import argparse
import time
import sklearn as sk
import cv2
import numpy as np
import json

from object.vehicule import DetectedObject
from object.vehicules import Vehicule

do: DetectedObject


def main(argv):
    parser = argparse.ArgumentParser()
    # Required arguments.
    parser.add_argument(
        "--file",
        help="Input video file.", )
    # Optional arguments.
    parser.add_argument(
        "--iou",
        default=0.2,
        help="threshold for tracking", )
    args = parser.parse_args()
    track('data/video/' + args.file, args.iou)


def overlap(box1, box2):
    """
    Check the overlap of two boxes
    """
    endx = max(box1[0] + box1[2], box2[0] + box2[2])
    startx = min(box1[0], box2[0])
    width = box1[2] + box2[2] - (endx - startx)

    endy = max(box1[1] + box1[3], box2[1] + box2[3])
    starty = min(box1[1], box2[1])
    height = box1[3] + box2[3] - (endy - starty)

    if (width <= 0 or height <= 0):
        return 0
    else:
        Area = width * height
        Area1 = box1[2] * box1[3]
        Area2 = box2[2] * box2[3]
        ratio = Area / (Area1 + Area2 - Area)
        return ratio


def get_ressemblance(od, tv):
    # feature vector of do:
    od_features = [od.center, *od.mean_colors]

    # feature vector of tv:
    if not tv.velocity:
        tv_features = [tv.center, *tv.mean_colors]
    else:
        tv_features = [tv.futur_center, *tv.mean_colors, tv.velocity]
        od_features.append(np.array(od.center - tv.center))

    return sk.metrics.mean_squared_error(tv_features, od_features)


def track(video, iou):
    # todo get frames with module 1
    camera = cv2.VideoCapture(video)
    res, frame = camera.read()
    y_size = frame.shape[0]
    x_size = frame.shape[1]

    frames = 0
    counter = 0
    tracked_vehicules = []
    cv2.namedWindow("detection", cv2.WINDOW_NORMAL)

    while True:
        frames += 1
        # take the next image from the database
        frame = cv2.imread("data/image/image" + str(frames) + ".jpg")
        # get the associated contour
        objects_detected = []
        with open("data/bounding_boxes/image" + str(frames) + ".json") as f:
            data = json.load(f)
            # For each detected object, add the newVehicules
            for elem in data:
                # if elem["proba"] > 50 :
                if elem["object"] == "truck" or elem["object"] == "car":
                    x = elem["left"]
                    y = elem["top"]
                    w = elem["right"] - elem["left"]
                    h = elem["bot"] - elem["top"]
                    objects_detected.append(DetectedObject((x, y, w, h), frame))

        # For each vehicules of the new frame
        for od in objects_detected:
            ressemblances = []
            for tv in tracked_vehicules:
                count = 0
                ressemblances.append(get_ressemblance(od,tv))
            if max(ressemblances) > 0.9
                counter += 1
            else:
                trackedVehicules.append(vehicule)
                counter += 1

        # Check and update goals
        if trackedVehicules:
            tlist = copy.copy(trackedVehicules)
            for e in tlist:
                x, y = e.center
                # todo set proper outofbound size
                if 0.05 * x_size < x < 0.95 * x_size and 0.05 * y_size < y < 0.95 * y_size:
                    e.update(frame)
                elif e.number_of_frame < 20:
                    e.update(frame)
                else:
                    trackedVehicules.remove(e)

        time.sleep(0.2)
        # Frame overlay
        cv2.putText(frame, "frame: " + str(frames), (0, 0 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(frame, "Counter: " + str(counter), (0, 0 + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,
                    cv2.LINE_AA)
        for i, e in enumerate(trackedVehicules):
            cv2.putText(frame, "tracked: " + str(e.center), (0, 0 + 60 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 1,
                        cv2.LINE_AA)

        cv2.imshow("detection", frame)

        if cv2.waitKey(110) & 0xff == 27:
            break
    camera.release()


if __name__ == '__main__':
    main(sys.argv)
