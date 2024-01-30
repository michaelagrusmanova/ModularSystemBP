# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 16:54:37 2021

@author: micha
"""
import cv2
import numpy as np

def method_erosion(previous, kernel, iteration):
    final_kernel = np.ones((kernel, kernel),np.uint8)
    erosion = cv2.erode(previous,final_kernel,iterations = iteration)
    return erosion
