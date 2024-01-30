# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 09:40:13 2021

@author: micha
"""
import cv2

def method_adaptive_thresh(previous,maxV, blockS, C_const, method):
    if blockS % 2 != 1:
        blockS += 1
    if blockS <= 1:
        blockS = 3
    if method == 1:
       th = cv2.adaptiveThreshold(previous, maxV, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockS, C_const)
    if method == 2:
       th = cv2.adaptiveThreshold(previous, maxV, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockS, C_const)
    return th