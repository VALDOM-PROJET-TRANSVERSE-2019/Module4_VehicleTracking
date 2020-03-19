"""
This module is the core tracking system
"""
import sys
import argparse
import json
import re
from os import listdir
from os.path import isfile, join

import numpy as np
from PIL import Image
from objects.vehicle import Vehicle
from objects.detectedobject import DetectedObject

NUMBERS = re.compile(r'(\d+)')


def main(argv):
    """
    :param argv: parser
    :return:
    """
    parser = argparse.ArgumentParser()
    # Required arguments.
    parser.add_argument(
        "--images",
        default="data/image/",
        help="Input images folder.", )
    # Optional arguments.
    parser.add_argument(
        "--boundingBoxes",
        default="data/bounding_boxes/",
        help="Bounding boxes folder", )
    parser.add_argument(
        "--detectionThreshold",
        default=0.2,
        help="Detection threshold value", )
    parser.add_argument(
        "--memoryFramesNumber",
        default=10,
        help="Detection threshold value", )
    args = parser.parse_args()

    track(args.images, args.boundingBoxes, args.detectionThreshold, args.memoryFramesNumber)


def numerical_sort(value):
    """
    :param value:
    :return:
    """
    parts = NUMBERS.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


def overlap(box1, box2):
    """
    Check the overlap of two boxes
    :param box1: (x,y,w,h) : (float, float, float, float)
    :param box2: (x,y,w,h) : (float, float, float, float)
    :return: 0 or overlap ratio between box1 and box2
    """
    end_x = max(box1[0] + box1[2], box2[0] + box2[2])
    start_x = min(box1[0], box2[0])
    width = box1[2] + box2[2] - (end_x - start_x)

    end_y = max(box1[1] + box1[3], box2[1] + box2[3])
    start_y = min(box1[1], box2[1])
    height = box1[3] + box2[3] - (end_y - start_y)

    if width <= 0 or height <= 0:
        return 0
    else:
        area = width * height
        area1 = box1[2] * box1[3]
        area2 = box2[2] * box2[3]
        ratio = area / (area1 + area2 - area)
        return ratio


def track(images_folder, bb_folder, detection_threshold=0.2, memory_frames_number=10):
    """
    :param images_folder: str, path to the images folder
    :param bb_folder: str, path to bounding_boxes folder
    :param detection_threshold:
    :param memory_frames_number: int,
    :return:
    """
    images = sorted([f for f in listdir(images_folder) if isfile(join(images_folder, f))], key=numerical_sort)
    bounding_boxes = sorted([f for f in listdir(bb_folder) if isfile(join(bb_folder, f))], key=numerical_sort)

    img_array = []
    bb_array = []
    vehicle_count = 0
    output_data = {}

    for image in images:
        img = Image.open(images_folder + image)
        img_array.append(np.asarray(img))
    for bb in bounding_boxes:
        with open(bb_folder + bb) as f:
            data = json.load(f)
        bb_array.append(data)

    detected_vehicles = []
    for i in range(len(img_array)):
        img = img_array[i]
        bbs = bb_array[i]
        detected_objects = []

        # Reset visibility
        for dv in detected_vehicles:
            dv.update_counter(False)
            if dv.counter > memory_frames_number:
                detected_vehicles.remove(dv)

        # Retrieve the different objects
        for o in bbs:
            if o['object'] == 'car' or o['object'] == 'truck':
                detected_objects.append(DetectedObject(o, img))

        # Delete overlaps
        for do1 in detected_objects:
            for do2 in detected_objects:
                if do1 != do2:
                    if overlap(do1.bounding_box, do2.bounding_box) > 0.6:
                        detected_objects.remove(do2)

        potential_vehicles_indexes = [i for i in range(len(detected_vehicles))]
        for do in detected_objects:
            found = False
            distances = []

            # Distances calculation
            for j in potential_vehicles_indexes:
                distances.append(do.get_distance_from(detected_vehicles[j]))

            if len(distances) != 0:
                shortest_distance = min(distances)
                shortest_distance_index = distances.index(shortest_distance)

                if shortest_distance < detection_threshold:
                    found = True
                    vehicle_index = potential_vehicles_indexes[shortest_distance_index]
                    detected_vehicles[vehicle_index].update_vehicle(do)

                    potential_vehicles_indexes.remove(potential_vehicles_indexes[shortest_distance_index])

            if not found:
                detected_vehicles.append(Vehicle(do, vehicle_count))
                vehicle_count += 1

        #print("Frame {}".format(i))
        #for dv in detected_vehicles:
         #   if dv.visible:
         #       dv.draw(img)

        output_data["frame " + str(i)] = [dv.id for dv in detected_vehicles]

    return output_data

    #for i in range(len(img_array)):
    #    cv2.imshow("detection", img_array[i])
     #   cv2.waitKey(200)


if __name__ == '__main__':
    main(sys.argv)
