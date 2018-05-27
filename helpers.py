# -*- coding: utf-8 -*-
"""
Created on Sun May 27 16:29:48 2018

@author: Yi (Robin) Fan
"""

import numpy as np
import cv2

#get histogram
def get_hist(img):
    bins = np.arange(0, 300, 10)
    bins[26] = 255
    hp = np.histogram(img, bins)
    return hp

#histogram reducing value
def get_hr(hp, sqrt_hw):
    for i in range(len(hp[0])):
        if hp[0][i] > sqrt_hw:
            return i * 10
        
#get contrast enhenced image
def get_CEI(img, hr, c):
    CEI = (img - (hr + 50 * c)) * 2
    CEI[np.where(CEI > 255)] = 255
    CEI[np.where(CEI < 0)] = 0
    return CEI
                
#draw image
def draw(img):
    tmp = img.astype(np.uint8)
    cv2.imshow('image',tmp)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()


#scale to 0 - 255
def scale(img):
   s = np.max(img) - np.min(img) 
   res = img / s
   res -= np.min(res)
   res *= 255
   return res

#get threshold for the avg edge image
def get_th(img, bins):
    hist = np.histogram(img,bins)
    peak_1_index = np.argmax(hist[0])
    peak_2_index = 0
    if peak_1_index == 0:
        peak_2_index += 1
    for i in range(len(hist[0])):
        if hist[0][i] > hist[0][peak_2_index] and i != peak_1_index:
            peak_2_index = i
    peak_1 = hist[1][peak_1_index]
    peak_2 = hist[1][peak_2_index]
    return ((peak_1 + peak_2) / 2), hist

def get_th2(img, bins):
    num = img.shape[0] * img.shape[1]
    hist = np.histogram(img, bins)
    cdf = 0
    for i in range(len(hist[0])):
        cdf += hist[0][i]
        if cdf / num > 0.85:
            return hist[1][i]

#threshold the image
def img_threshold(th, img, flag):
    h = img.shape[0]
    w = img.shape[1]
    new_img = np.zeros((h,w))
    if flag == "H2H":
        new_img[np.where(img >= th)] = 255
    elif flag == "H2L":
        new_img[np.where(img < th)] = 255
    return new_img

# merge cei and edge map
def merge(edge, cei):
    h = edge.shape[0]
    w = edge.shape[1]
    new_img = 255 * np.ones((h,w))

    new_img[np.where(edge == 255)] = 0
    new_img[np.where(cei == 255)] = 0
    return new_img

def find_end(tli, x, y):
    i = x
    while(i < tli.shape[0] and tli[i][y] == 0):
        i += 1
    return i - 1

def find_mpv(cei, head, end, y):
    h = []
    e = []
    for k in range(5):
        if head - k >= 0:
            h.append(cei[head-k][y])
        if end + k < cei.shape[0]:
            e.append(cei[end + k][y])
    return np.max(h), np.max(e)
    
    
# set interpolated image
def set_intp_img(img, x, y, tli, cei):
    head = x
    end = find_end(tli, x, y)
    n = end - head + 1
    if n > 30:
        return end
    mpv_h, mpv_e = find_mpv(cei, head, end, y)
    for m in range(n):
        img[head+m][y] = mpv_h + (m + 1) * ((mpv_e - mpv_h) / n) 
    return end
    