# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 11:13:38 2021

@author: micha
"""
import cv2
import modul_resize

def method_toycbcr(required_size, path, number):
    img = cv2.imread(path)
    image = modul_resize.resizing(img, required_size)
    YCrCb = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
    Y = YCrCb[:,:,number]
    return Y