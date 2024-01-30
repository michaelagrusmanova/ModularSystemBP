# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 16:58:52 2021

@author: micha
"""
import cv2
import numpy as np

def method_dilation(previous, kernel, iteration):
    final_kernel = np.ones((kernel, kernel),np.uint8)
    dilation = cv2.dilate(previous,final_kernel,iterations = iteration)
    return dilation
