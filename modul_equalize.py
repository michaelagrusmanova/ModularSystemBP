# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 14:19:46 2021

@author: micha
"""
import cv2

def method_equalize(previous):
    equ = cv2.equalizeHist(previous, 0)
    return equ