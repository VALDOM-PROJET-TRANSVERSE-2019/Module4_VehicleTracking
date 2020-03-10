
import sys
import copy
import argparse
import cv2
import numpy as np
import json

from object.vehicules import Vehicule


def main(argv):
    parser = argparse.ArgumentParser()
    # Required arguments.
    parser.add_argument(
        "--file",
        help="Input video file.",
    )
    # Optional arguments.
    parser.add_argument(
        "--iou",
        default=0.2,
        help="threshold for tracking",
    )
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


def track(video, iou):
    #todo get frames with module 1
    camera = cv2.VideoCapture(video)
    res, frame = camera.read()
    y_size = frame.shape[0]
    x_size = frame.shape[1]

    frames = 0
    counter = 0
    track_list = []
    cv2.namedWindow("detection", cv2.WINDOW_NORMAL)

    while True:
        frames += 1
        # take the next image from the database
        frame = cv2.imread("data/image/image" + str(frames) + ".jpg")
        # get the associated contour
        contours = []
        with open("data/bounding_boxes/image" + str(frames) + ".json") as f:
            data = json.load(f)
            for elem in data:
                if elem["proba"] > 70:
                    x = elem["left"]
                    y = elem["top"]
                    w = elem["right"] - elem["left"]
                    h = elem["bot"] - elem["top"]
                    contours.append((x, y, w, h))

        # Check the bouding boxs
        for c in contours:
            vehicule = Vehicule(counter, (x, y, w, h), frame)

            # Exclude existing targets in the tracking list
            if track_list:
                count = 0
                num = len(track_list)
                for p in track_list:
                    # if new contours overlap with current tracked
                    #todo add other condition for vehicule existence
                    if overlap((x, y, w, h), p.bounding_box) < iou:
                        count += 1
                if count == num:
                    track_list.append(vehicule)
                    counter += 1
            else:
                track_list.append(vehicule)
                counter += 1

        # Check and update goals
        if track_list:
            tlist = copy.copy(track_list)
            for e in tlist:
                x, y = e.center
                #todo set proper outofbound size
                if 0.1 * x_size < x < 0.9 * x_size and 0.1 * y_size < y < 0.9 * y_size:
                    e.update(frame)
                else:
                    track_list.remove(e)
        cv2.putText(frame, "frame: "+ str(frames), (0, 0 +20 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, "Counter: " + str(counter), (0, 0 + 40 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

        cv2.imshow("detection", frame)

        if cv2.waitKey(110) & 0xff == 27:
            break
    camera.release()


if __name__ == '__main__':
    main(sys.argv)
