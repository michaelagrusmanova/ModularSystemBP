# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 11:27:08 2021

@author: micha
"""
import imutils

def method_rotate(previous, angles):
    rotated = imutils.rotate_bound(previous, angles)
    return rotated

