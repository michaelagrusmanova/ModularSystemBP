# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 18:11:35 2021

@author: micha
"""
import cv2
import numpy as np

def method_top_hat(previous, kernel):
    final_kernel = np.ones((kernel, kernel),np.uint8)
    tophat = cv2.morphologyEx(previous, cv2.MORPH_TOPHAT, final_kernel)
    return tophat