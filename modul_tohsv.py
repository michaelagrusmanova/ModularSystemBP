# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 11:24:03 2021

@author: micha
"""
import cv2
import modul_resize

def method_tohsv(required_size, path, number):
    img = cv2.imread(path)
    image = modul_resize.resizing(img, required_size)
    HSV = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    H = HSV[:,:,number]
    return H
    