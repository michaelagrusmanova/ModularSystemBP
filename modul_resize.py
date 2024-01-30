# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 11:00:05 2021

@author: micha
"""
import cv2


def resizing(img, required_size):
    """
    Resizes the image to required size (internally is set 400px)
    To maintaining the ratio, the width or height is automatically calculated.
    Parameters
    ----------
    img : image
    ----------
    Returns resized image
    """
    """
    Resizes the image to required size (internally is set 400px)
    To maintaining the ratio, the width or height is automatically calculated.
    Parameters
    ----------
    img : image
    ----------
    Returns resized image
    """
    width = img.shape[1]
    height = img.shape[0]
    if(width > height):
        new_width = required_size
        new_height = int(new_width * height / width)
    else:
        new_height = required_size
        new_width =int(new_height * width / height)
    dim = (new_width, new_height)
    image = cv2.resize(img, dim, fx = 0.1, fy = 0.1)
    return image
