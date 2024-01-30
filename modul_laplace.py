# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 09:56:28 2021

@author: micha
"""
import cv2

def method_laplace(previous):
    laplacian = cv2.Laplacian(previous,cv2.CV_64F)
    img = cv2.convertScaleAbs(laplacian)
    return img