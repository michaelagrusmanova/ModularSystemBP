# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 12:44:25 2021

@author: micha
"""
import cv2
import numpy as np
import modul_resize

def method_hough_transform(previous, linelength, linegap, threshold):
    cimg = previous
    gray = previous
    #cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    edges = cv2.Canny(gray, 50, 200)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold, minLineLength=linelength, maxLineGap=linegap)
    for line in lines:
       x1, y1, x2, y2 = line[0]
       cv2.line(cimg, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return cimg

def method_hought_circle(previous, p1, p2):
    cimg = previous
    img = cv2.medianBlur(cimg,5)
    #cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
                                param1=p1,param2=p2,minRadius=0,maxRadius=0)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
    return cimg