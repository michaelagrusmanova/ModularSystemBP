# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 10:23:39 2021

@author: micha
"""
import cv2

def method_canny(previous, number):
    edges = cv2.Canny(previous,number,200)
    return edges