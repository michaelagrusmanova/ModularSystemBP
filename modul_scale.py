# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 13:42:55 2021

@author: micha
"""
import cv2

def method_scale(previous, percent):
    width = int(previous.shape[1] * percent / 100)
    height = int(previous.shape[0] * percent / 100)
    dsize = (width, height)
    res = cv2.resize(previous, dsize,fx=0.1, fy=0.1, interpolation = cv2.INTER_CUBIC)
    return res