import cv2

def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
    hasFrames, image = vidcap.read()
    if hasFrames:
        cv2.imwrite("image/" "image" + str(count) + ".jpg", image)  # save frame as JPG file
    return hasFrames


vidcap = cv2.VideoCapture('video/car.flv')
sec = 0
frameRate = 0.1  # it will capture image in each 0.5 second
count = 1
success = getFrame(sec)
while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)
