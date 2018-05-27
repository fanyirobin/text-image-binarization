# -*- coding: utf-8 -*-
"""
Created on Wed May  2 15:33:52 2018

@author: Yi (Robin) Fan
"""
#%% Parameters for user
c = 0.4                   # in the range[0, 1] recommend 0.2-0.3
bl = 260                # range[230 - 300]  recommend 260

#%% get File
print("Please Input File Name (Example: image_name)")     
FILE_NAME = input("FILE_NAME: ")
print("Please Input File Format (Example: .png)") 
FORMAT = input("FORMAT: ")

#%% Program begin here
import cv2
import numpy as np
from helpers import *

im = cv2.imread(FILE_NAME + FORMAT)
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
gray = gray.astype(np.float32)

width = gray.shape[1]
height = gray.shape[0]

#%% STEP: contrast enhancement
print("Enhancing Contrast")
hp = get_hist(im)
sqrt_hw = np.sqrt(height * width)
hr = get_hr(hp, sqrt_hw)
cei = get_CEI(gray, hr, c)
cv2.imwrite(FILE_NAME + "_Cei" + FORMAT, cei)

#%% STEP: Edge detection
print("Edge Detection")
# build four filters
m1 = np.array([-1,0,1,-2,0,2,-1,0,1]).reshape((3,3))
m2 = np.array([-2,-1,0,-1,0,1,0,1,2]).reshape((3,3))
m3 = np.array([-1,-2,-1,0,0,0,1,2,1]).reshape((3,3))
m4 = np.array([0,1,2,-1,0,1,-2,-1,0]).reshape((3,3))

eg1 = np.abs(cv2.filter2D(gray, -1, m1))
eg2 = np.abs(cv2.filter2D(gray, -1, m2))
eg3 = np.abs(cv2.filter2D(gray, -1, m3))
eg4 = np.abs(cv2.filter2D(gray, -1, m4))
eg_avg = scale((eg1 + eg2 + eg3 + eg4) / 4)

bins_1 = np.arange(0, 265, 5) 
#threshold = get_th2(eg_avg, bins_1)
eg_bin = img_threshold(30, eg_avg,"H2H") #threshold is hard coded to 30 (based 
                                         #on the paper). Uncomment above to replace
cv2.imwrite(FILE_NAME + "_EdgeBin" + FORMAT, eg_bin)


#%% STEP: Text location
print("Locating the Text")
bins_2 = np.arange(0, 301, 40)
#threshold_c = 255 - get_th2(cei, bins_2)
cei_bin = img_threshold(60, cei, "H2L")#threshold is hard coded to 60 (based 
                                       #on the paper). Uncomment above to replace
cv2.imwrite(FILE_NAME + "_CeiBin" + FORMAT, cei_bin)
tli = merge(eg_bin, cei_bin)
cv2.imwrite(FILE_NAME + "_TLI" + FORMAT, tli)
kernel = np.ones((3,3),np.uint8)
erosion = cv2.erode(tli,kernel,iterations = 1)
cv2.imwrite(FILE_NAME + "_TLI_erosion" + FORMAT, erosion)


#%% STEP: Light distribution
print("Estimate Light Distribution")
int_img = np.array(cei)
ratio = int(width / 20)
for y in range(width):
    if y % ratio == 0 :
        print(int(y / width * 100), "%")
    for x in range(height):
        if erosion[x][y] == 0:
            x = set_intp_img(int_img, x, y, erosion, cei)
mean_filter = 1 / 121 * np.ones((11,11), np.uint8)
ldi = cv2.filter2D(scale(int_img), -1, mean_filter)
cv2.imwrite(FILE_NAME + "_LDI" + FORMAT, ldi)


#%% STEP: Light Balancing
print("Balancing Light and Generating Result")
result = np.divide(cei, ldi) * bl
result[np.where(erosion != 0)] *= 1.5

cv2.imwrite(FILE_NAME + "_result" + FORMAT, result)