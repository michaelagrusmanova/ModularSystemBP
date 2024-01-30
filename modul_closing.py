# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 17:02:15 2021

@author: micha
"""
import cv2
import numpy as np

def method_closing(previous, kernel):
    final_kernel = np.ones((kernel, kernel),np.uint8)
    closing = cv2.morphologyEx(previous, cv2.MORPH_CLOSE, final_kernel)
    return closing
