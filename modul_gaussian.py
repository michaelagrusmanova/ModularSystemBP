# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 15:26:14 2021

@author: micha
"""
import cv2
import modul_helpers

def method_gaussian(previous, number):
    numb = modul_helpers.check_odd(number)
    blur = cv2.GaussianBlur(previous,(numb,numb),0)
    return blur