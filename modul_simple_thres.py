# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 09:40:13 2021

@author: micha
"""
import cv2

def method_simple_thresh(previous, n1, n2, method):
    if method == 1:
       ret,thresh1 = cv2.threshold(previous, n1, n2,cv2.THRESH_BINARY)
    if method == 2:
       ret,thresh1 = cv2.threshold(previous, n1, n2,cv2.THRESH_BINARY_INV)
    if method == 3:
       ret,thresh1 = cv2.threshold(previous, n1, n2,cv2.THRESH_TRUNC)
    if method == 4:
       ret,thresh1 = cv2.threshold(previous, n1, n2,cv2.THRESH_TOZERO)
    if method == 5:
       ret,thresh1 = cv2.threshold(previous, n1, n2,cv2.THRESH_TOZERO_INV)
    return thresh1