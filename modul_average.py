# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 15:12:41 2021

@author: micha
"""
import cv2
import modul_helpers

def method_average(previous, number):
    numb = modul_helpers.check_odd(number)
    blur = cv2.blur(previous, (numb,numb))
    return blur

