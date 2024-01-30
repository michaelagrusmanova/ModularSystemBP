# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 17:00:00 2021

@author: micha
"""
import cv2
import numpy as np

def method_opening(previous, kernel):
    final_kernel = np.ones((kernel, kernel),np.uint8)
    opening = cv2.morphologyEx(previous, cv2.MORPH_OPEN, final_kernel)
    return opening
