# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 14:16:19 2021

@author: micha
"""
import cv2

def method_negate(previous):
    negative = 255 - previous
    return negative