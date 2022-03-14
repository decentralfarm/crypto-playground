from __future__ import print_function
from __future__ import division
import cv2 as cv
import numpy as np
import argparse
import os
import config

def compareImages(src, samples_dir):
    src_img = cv.imread(src)
    hsv_base = cv.cvtColor(src_img, cv.COLOR_BGR2HSV)
    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]
    # hue varies from 0 to 179, saturation from 0 to 255
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges # concat lists
    # Use the 0-th and 1-st channels
    channels = [0, 1]
    hist_base = cv.calcHist([hsv_base], channels, None, histSize, ranges, accumulate=False)
    cv.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
    min_distance = 1
    max_distance = 0
    for file in os.listdir(samples_dir):
        print(f"filename: {file}")
        image = cv.imread(config.DEC_IMGS_DIR+file)
        hsv_sample = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        hist_sample = cv.calcHist([hsv_sample], channels, None, histSize, ranges, accumulate=False)
        cv.normalize(hist_sample, hist_sample, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
        distance = cv.compareHist(hist_base, hist_sample, 3)
        
        min_distance = min(distance, min_distance)
        max_distance = max(distance, max_distance)
        print(f"dist: {distance}")
        print(f"min dist: {min_distance}")
        print(f"max dist: {max_distance}")
    return (min_distance, max_distance)
       


