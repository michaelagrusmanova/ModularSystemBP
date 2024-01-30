# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 09:40:13 2021

@author: micha
"""
import cv2

def method_otsu_thresh(previous, thresh, maxValue):
    ret2,th2 = cv2.threshold(previous,thresh,maxValue,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return th2