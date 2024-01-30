# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 10:02:26 2021

@author: micha
"""
from scipy.ndimage import label
import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
import scipy.ndimage as ndimage
from PIL import Image


def method_coloring(image):
    #img = cv2.imread("20160516_134433.jpg")
    #ret, bw_img = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    # plt.imshow(img)
    lbl, ncc = label(image)
    
    #print(ncc)
    #print(lbl)
    #plt.imshow(lbl)
    #return lbl.astype("uint8") +- funguje
    return lbl.astype("uint8")

    