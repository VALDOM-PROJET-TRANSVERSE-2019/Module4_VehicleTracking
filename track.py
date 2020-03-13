import hashlib
import sys
import copy
import argparse
import cv2

from object.vehicules import Vehicule

def main(argv):
    parser = argparse.ArgumentParser()
    # Required arguments.
    parser.add_argument(
        "--file",
        default= "car.flv",
        help="Input video file.", )
    # Optional arguments.
    parser.add_argument(
        "--iou",
        default=0.05,
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

def track(video, iou):
    camera = cv2.VideoCapture(video)
    res, frame = camera.read()
    y_size = frame.shape[0]
    x_size = frame.shape[1]
    bs = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

    history = 10
    frames = 0
    counter = 0

    tracked_vehicules = []
    unique = []
    cv2.namedWindow("detection", cv2.WINDOW_NORMAL)

    while True:
        res, frame = camera.read()
        if not res:
            break
        fg_mask = bs.apply(frame)
        if frames < history:
            frames += 1
            continue
        th = cv2.threshold(fg_mask.copy(), 244, 255, cv2.THRESH_BINARY)[1]
        th = cv2.erode(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
        dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
        contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            print(cv2.contourArea(c))
            x, y, w, h = cv2.boundingRect(c)
            if cv2.contourArea(c) > 2000:
                if tracked_vehicules:
                    count = 0
                    num = len(tracked_vehicules)
                    for tv in tracked_vehicules:
                        if overlap((x, y, w, h), tv.bounding_box) < iou:
                            count += 1
                    if count == num:
                        counter += 1
                        tracked_vehicules.append(
                            Vehicule(hashlib.blake2s(str(c).encode(), key=b'AP', digest_size=3).hexdigest(),
                                     (x, y, w, h), frame))
                else:
                    counter += 1
                    tracked_vehicules.append(
                        Vehicule(hashlib.blake2s(str(c).encode(), key=b'AP', digest_size=3).hexdigest(), (x, y, w, h),
                                 frame))

        # Check and update goals
        if tracked_vehicules:
            tlist = copy.copy(tracked_vehicules)
            for tv in tlist:
                xc, yc = tv.center
                if x_size*0.20 < xc+tv.w < x_size*0.99 and 10 < yc < y_size*0.9:
                    tv.update(frame)
                else:
                    tracked_vehicules.remove(tv)
                    if tv.updated:
                        unique.append(tv.get_id())


        # Frame overlay
        cv2.rectangle(frame, (x_size - 40, y_size - 10), (40, 10), (0, 255, 255), 1)
        cv2.putText(frame, "Frame #: " + str(frames), (5, 5 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(frame, "Unique : " + str(len(unique)), (5, 5 + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(frame, "Tracked: ", (5, 5 + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 1,
                    cv2.LINE_AA)

        for i, e in enumerate(tracked_vehicules):
            cv2.putText(frame, str(e.get_id()), (7, 7 + 75 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 1,
                        cv2.LINE_AA)

        frames += 1
        cv2.imshow("detection", frame)

        if cv2.waitKey(110) & 0xff == 27:
            break
    camera.release()


if __name__ == '__main__':
    main(sys.argv)
