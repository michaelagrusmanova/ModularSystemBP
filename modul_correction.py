# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 13:56:21 2021

@author: micha
"""
import cv2
from numpy import zeros, newaxis


def method_correct(previous, etalon, c):
    if len(previous.shape)== 2:
        prev = previous[..., newaxis]
    else:
        prev = previous
        
    g = prev.astype(float) * c / etalon.astype(float)
    result = cv2.cvtColor(g.astype('uint8'), cv2.COLOR_RGB2BGR)
    
    return result