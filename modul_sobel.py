# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 10:03:05 2021

@author: micha
"""
import cv2

def method_sobel(previous, number):
    sobel = cv2.Sobel(previous,cv2.CV_8U,1,0,ksize=number)
    return sobel