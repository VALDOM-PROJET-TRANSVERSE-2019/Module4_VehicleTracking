"""
This module is the core tracking system
"""
import json
import re
from os import listdir
from os.path import isfile, join

import imageio
import numpy as np
from pygifsicle import optimize
from PIL import Image
from tracker.objects import DetectedObject
from tracker.objects import Vehicle


def numerical_sort(value):
    """
    :param value:
    :return:
    """
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
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


def track(images_folder, bb_folder, detection_threshold, memory_frames_number=10):
    """
    :param images_folder: str, path to the images folder
    :param bb_folder: str, path to bounding_boxes folder
    :param detection_threshold:
    :param memory_frames_number: int,
    :return:
    """
    images = sorted([f for f in listdir(images_folder) if isfile(join(images_folder, f))],
                    key=numerical_sort)

    img_array = []
    img_pil = []
    bb_array = []
    vehicle_count = 0
    output_data = {}

    for image in images:
        img = Image.open(images_folder + image)
        img_pil.append(img)
        img_array.append(np.asarray(img))

    # Instantiate bounding_boxes
    if str(bb_folder)[-5:] == ".json":
        # Open as it is a json
        try:
            data_file = json.load(open(bb_folder, 'r'))
            for content in data_file.values():
                bb_array.append(content)
        except IsADirectoryError:
            print("Provide a json file or similar")
            return "Provide a json file or similar"
    else:
        # Open as it is a dictionnary
        try:
            data_file = json.loads(bb_folder)
        except TypeError:
            data_file = bb_folder
        for content in data_file.values():
            print(type(content))
            bb_array.append(content)

    detected_vehicles = []
    for i, (img, pil, bbs) in enumerate(zip(img_array, img_pil, bb_array)):
        detected_objects = []

        # Reset visibility
        for d_v in detected_vehicles:
            d_v.update_counter(False)
            if d_v.get_counter() > memory_frames_number:
                detected_vehicles.remove(d_v)

        # Retrieve the different objects
        print(type(bbs))
        for obj in bbs:
            if obj['object'] == 'car' or obj['object'] == 'truck':
                detected_objects.append(DetectedObject(obj, img))

        # Delete overlaps
        for do_1 in detected_objects:
            for do_2 in detected_objects:
                if do_1 != do_2:
                    if overlap(do_1.get_coordinate(), do_2.get_coordinate()) > 0.6:
                        detected_objects.remove(do_2)

        potential_vehicles_indexes = [i for i in range(len(detected_vehicles))]

        for d_o in detected_objects:
            found = False
            distances = []

            # Distances calculation
            for j in potential_vehicles_indexes:
                distances.append(d_o.get_distance_from(detected_vehicles[j]))

            if distances:
                shortest_distance = min(distances)
                shortest_distance_index = distances.index(shortest_distance)

                if shortest_distance < detection_threshold:
                    found = True
                    vehicle_index = potential_vehicles_indexes[shortest_distance_index]
                    detected_vehicles[vehicle_index].update_vehicle(d_o)
                    potential_vehicles_indexes.remove(potential_vehicles_indexes[shortest_distance_index])

            if not found:
                detected_vehicles.append(Vehicle(d_o, vehicle_count))
                vehicle_count += 1

        for d_v in detected_vehicles:
            if d_v.get_visible():
                d_v.draw(pil)

        output_data["frame " + str(i)] = [d_v.get_id() for d_v in detected_vehicles if d_v.get_visible()]

    return output_data

    imageio.mimsave('output.gif', img_pil)
    optimize("output.gif")
