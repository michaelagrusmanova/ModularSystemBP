# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 10:04:40 2021

@author: micha
"""
import cv2
import numpy as np
import modul_resize

def method_searching(previous, template, method):
    w, h = template.shape[::-1]
    if method == 1:
        img2 = previous.copy()    
    # # All the 6 methods for comparison in a list
    # methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
    #             'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
        img = img2.copy()
        method = eval('cv2.TM_CCOEFF_NORMED')
        # Apply template Matching
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        # if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        #     top_left = min_loc
        # else:
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        cv2.rectangle(img,top_left, bottom_right, (0, 255, 0),2)
        # plt.subplot(121),plt.imshow(res,cmap = 'gray')
        # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        # plt.subplot(122),plt.imshow(img,cmap = 'gray')
        # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        #plt.suptitle(meth)
    else:
        img = previous
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,255,0), 2)
    return img



    