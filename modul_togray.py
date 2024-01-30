# -*- coding: utf-8 -*-
"""
@author: micha
"""
import cv2
import modul_resize

def method_togray(required_size, path):
    img = cv2.imread(path) 
    image = modul_resize.resizing(img, required_size)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray
