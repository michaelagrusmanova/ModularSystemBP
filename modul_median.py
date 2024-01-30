# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 20:39:20 2021

@author: micha
"""
import cv2
import modul_helpers

def method_median(previous, number):
    numb = modul_helpers.check_odd(number)
    median = cv2.medianBlur(previous, numb)
    return median
