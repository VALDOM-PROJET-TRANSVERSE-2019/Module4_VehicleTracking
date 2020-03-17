# coding:utf8

"""
Description :
Class for the tracked vehicule.
"""
import cv2
import numpy as np


class DetectedObject(object):
    def __init__(self, bounding_box, frame):
        
        self.frame_size = (len(frame[0]),len(frame))
        self.x = bounding_box['left']
        self.y = bounding_box['top']
        self.w = bounding_box['right'] - bounding_box['left']
        self.h = bounding_box['bot'] - bounding_box['top']
        self.bounding_box = self.x, self.y, self.w, self.h

        self.center = [self.x + self.w/2,self.y + self.h/2]
        self.direction = None
        self.updated = False
        
        self.get_mean_color(frame)


    def get_mean_color(self,frame):
        frame_zone = frame[self.y:self.y+self.h,self.x:self.x+self.w]
        frame_zone = np.array(frame_zone)
        color_r = np.mean(frame_zone[:,:,0]) / 255
        color_g = np.mean(frame_zone[:,:,1]) / 255
        color_b = np.mean(frame_zone[:,:,2]) / 255
        self.mean_colors = (color_r,color_g,color_b)


    def get_distance_from(self,vehicule):
        do_array = self.get_feature_array()
        dv_array = vehicule.get_feature_array()

        dist = np.linalg.norm(do_array-dv_array)

        return dist

    def get_feature_array(self):
        x = self.x / self.frame_size[0]
        y = self.y / self.frame_size[1]
        w = self.w / self.frame_size[0]
        h = self.h / self.frame_size[1]
        r = self.mean_colors[0] / 255
        g = self.mean_colors[1] / 255
        b = self.mean_colors[2] / 255
        return np.array([x,y,w,h,r,g,b])
        