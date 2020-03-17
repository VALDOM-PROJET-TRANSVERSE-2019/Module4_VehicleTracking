import hashlib
import sys
import copy
import argparse
import cv2
import json
import requests
import copy
from os import listdir
from os.path import isfile, join

from object.vehicule2 import Vehicule2
from object.DetectedObject import DetectedObject

import re
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def main(argv):
    parser = argparse.ArgumentParser()
    # Required arguments.
    parser.add_argument(
        "--images",
        default= "data/image/",
        help="Input images folder.", )
    # Optional arguments.
    parser.add_argument(
        "--boundingBoxes",
        default="data/bounding_boxes/",
        help="Boudingboxes folder", )
    parser.add_argument(
        "--detectionThreshold",
        default=0.2,
        help="Detection threshold value", )
    parser.add_argument(
        "--memoryFramesNumber",
        default=10,
        help="Detection threshold value", )
    args = parser.parse_args()

    images = sorted([f for f in listdir(args.images) if isfile(join(args.images, f))],key=numericalSort)
    bounding_boxes = sorted([f for f in listdir(args.boundingBoxes) if isfile(join(args.boundingBoxes, f))],key=numericalSort)

    track(args.images,images,args.boundingBoxes,bounding_boxes,args.detectionThreshold,args.memoryFramesNumber)


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

def track(images_folder, images, bb_folder, bounding_boxes, detection_threshold, memory_frames_number):
    img_array = []
    bb_array = []
    vehicule_count = 0

    for image in images:
        img = cv2.imread(images_folder+image)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    for bb in bounding_boxes:
        with open(bb_folder+bb) as f:
            data = json.load(f)
        bb_array.append(data)

    detectedVehicules = []    
    for i in range(len(img_array)):
    # for i in range(20,35,1):
        img = img_array[i]
        bbs = bb_array[i]
        detectedObjects = []

        # Reset visibility
        for dv in detectedVehicules:
            dv.update_counter(False)
            if dv.counter > memory_frames_number:
                detectedVehicules.remove(dv)
                

        # Retrieve the different objects
        for o in bbs:
            if(o['object']=='car' or o['object']=='truck'):
                detectedObjects.append(DetectedObject(o,img))

        # Delete overlaps
        for do1 in detectedObjects:
            for do2 in detectedObjects:
                if(do1!=do2):
                    if(overlap(do1.bounding_box, do2.bounding_box) > 0.6):
                        detectedObjects.remove(do2)


        potential_vehicules_indexes = [i for i in range(len(detectedVehicules))]
        for do in detectedObjects:
            found = False
            distances = []

            # Distances calculation
            for j in potential_vehicules_indexes:
                distances.append(do.get_distance_from(detectedVehicules[j]))

            if(len(distances)!=0):
                shortest_distance = min(distances)
                shortest_distance_index = distances.index(shortest_distance)

                if(shortest_distance < detection_threshold):
                    found = True
                    vehicule_index = potential_vehicules_indexes[shortest_distance_index]
                    # detectedVehicules[vehicule_index] = Vehicule2(do,detectedVehicules[vehicule_index].id)
                    detectedVehicules[vehicule_index].update_vehicule(do)

                    potential_vehicules_indexes.remove(potential_vehicules_indexes[shortest_distance_index])

            if not found : 
                detectedVehicules.append(Vehicule2(do,vehicule_count))
                vehicule_count += 1

        
        print("Frame {}".format(i))
        for dv in detectedVehicules:
            if(dv.visible):
                dv.draw(img)
    
    for i in range(len(img_array)):
    # for i in range(20,35,1):
        cv2.imshow("detection",img_array[i])
        cv2.waitKey(200)


if __name__ == '__main__':
    main(sys.argv)

