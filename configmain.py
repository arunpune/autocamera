#-*- coding: utf-8 -*-
# used for relative path calculation

#import imquality.brisque as brisque
import imquality.brisque as brisque
import traceback
import warnings
from configparser import ConfigParser
#from brisque import BRISQUE
from brisque import BRISQUE
import cv2
import json
import os
import math
import csv
import pandas as pd
import ast
from flask import Flask

#from flask_restful import Api, Resource, reqparse
from flask_restful import Api, Resource, reqparse



import numpy as np
from skimage import img_as_float, io
from skimage.metrics import structural_similarity as ssim
#this is used in the rotation function
from math import atan2, cos, sin, sqrt, pi



BASE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
CSV_PATH = os.path.join(os.getcwd(),'result.csv')
print(CSV_PATH)
# reading config.ini file
config = ConfigParser()
config.read('./config.ini')

# image dimensions
IMG_WIDTH = int(config['IMAGEDIMENSIONS']['IMG_WIDTH'])
IMG_HEIGHT = int(config['IMAGEDIMENSIONS']['IMG_HEIGHT'])

# blur threshold for laplcaian blur
LAP_THRESHOLD_BLUR = int(config['BLUR']['BLUR_LAP_THRESHOLD'])

# scrolling thresholds
SCROLL_THRESHOLD_1 = int(config['SCROLLING']['SCROLL_THRESHOLD_1'])
SCROLL_THRESHOLD_2 = int(config['SCROLLING']['SCROLL_THRESHOLD_2'])
SCROLL_COLORCNT_PCT = int(config['SCROLLING']['SCROLL_COLORCOUNT_PCT'])

# alignment thresholds
ALIGN_PERFECT_M_THRESHOLD = int(
    config['ALIGNMENT']['ALIGN_PERFECT_M_THRESHOLD'])
ALIGN_INVERTM_1 = int(config['ALIGNMENT']['ALIGN_INVERT_M1'])
ALIGN_INVERTM_2 = int(config['ALIGNMENT']['ALIGN_INVERT_M2'])
NOT_ALIGN_M1 = int(config['ALIGNMENT']['NOT_ALIGN_M1'])
NOT_ALIGN_M2 = int(config['ALIGNMENT']['NOT_ALIGN_M2'])

# mirror thresholds
MIRROR_THRESHOLD = float(config['MIRROR']['MIRROR_THRESHOLD'])

# static lines thresholds
STATIC_LINES_THRESHOLD = float(config['STATICLINES']['STATIC_LINES_THRESHOLD'])
STATIC_LINES_THRESHOLD_0 = int(
    config['STATICLINES']['STATIC_LINES_THRESHOLD_0'])
STATIC_LINES_THRESHOLD_1 = int(
    config['STATICLINES']['STATIC_LINES_THRESHOLD_1'])
STATIC_LINES_THRESHOLD_2 = int(
    config['STATICLINES']['STATIC_LINES_THRESHOLD_2'])
STATIC_LINES_MIN_LINE_LEN = int(
    config['STATICLINES']['STATIC_LINES_MIN_LINE_LEN'])
STATIC_LINES_MAX_LINE_GAP = int(
    config['STATICLINES']['STATIC_LINES_MAX_LINE_GAP'])
STATIC_LINES_RHO = int(config['STATICLINES']['STATIC_LINES_RHO'])

# rotation thresholds
ROTATION_THRESHOLD_1 = int(config['ROTATION']['ROTATION_THRESHOLD_1'])
ROTATION_THRESHOLD_2 = int(config['ROTATION']['ROTATION_THRESHOLD_2'])
ROTATION_MIN_LINE_LEN = int(config['ROTATION']['ROTATION_MIN_LINE_LEN'])
ROTATION_MAX_LINE_GAP = int(config['ROTATION']['ROTATION_MAX_LINE_GAP'])
ROTATION_THRESHOLD = int(config['ROTATION']['ROTATION_THRESHOLD'])
ROTATION_ANGLE_THRESHOLD_DEG = int(
    config['ROTATION']['ROTATION_ANGLE_THRESHOLD_DEG'])

# noise thresholds
NOISE_SAT_THRESHOLD_PCT = float(
    config['NOISE']['NOISE_SAT_THRESHOLD_PCT'])
NOISE_SAT_THRESHOLD = float(config['NOISE']['NOISE_SAT_THRESHOLD'])

# shift thresholds
LEFT_SHIFT_THRESHOLD_PER = int(
    config['IMAGE_SHIFTING']['LEFT_SHIFT_THRESHOLD_PER'])
RIGHT_SHIFT_THRESHOLD_PER = int(
    config['IMAGE_SHIFTING']['RIGHT_SHIFT_THRESHOLD_PER'])
TOP_SHIFT_THRESHOLD_PER = int(
    config['IMAGE_SHIFTING']['TOP_SHIFT_THRESHOLD_PER'])
BOTTOM_SHIFT_THRESOLD_PER = int(
    config['IMAGE_SHIFTING']['BOTTOM_SHIFT_THRESOLD_PER'])
SHIFT_AREA_THRESHOLD_PER = int(
    config['IMAGE_SHIFTING']['SHIFT_AREA_THRESHOLD_PER'])
OBJ_SCALE_FACTOR = float(config['IMAGE_SHIFTING']['OBJ_SCALE_FACTOR'])
OBJ_MIN_NEIGHBORS = int(config['IMAGE_SHIFTING']['OBJ_MIN_NEIGHBORS'])
OBJ_MIN_SIZE = eval(config['IMAGE_SHIFTING']['OBJ_MIN_SIZE'])
OBJ_MAX_SIZE = eval(config['IMAGE_SHIFTING']['OBJ_MAX_SIZE'])
CASCADE_PATH = config['IMAGE_SHIFTING']['CASCADE_PATH']

# ssim score thresholds
SSIM_SCORE_THRESHOLD_PCT = int(
    config['SSIM_SCORE']['SSIM_SCORE_THRESHOLD_PCT'])

# brisque score threshold
BRISQUE_SCORE_THRESHOLD_PCT = int(
    config['BRISQUE_SCORE']['BRISQUE_SCORE_THRESHOLD_PCT'])

# not_cropped_in_roi threshold
NOT_CROPPED_IN_ROI_THRESHOLD_PCT = int(
    config['NOT_CROPPED_IN_ROI']['NOT_CROPPED_IN_ROI_THRESHOLD_PCT'])

# initialize cascade object detector
cascade = cv2.CascadeClassifier(CASCADE_PATH)

# initialize BRISQUE score calculator obj
brisque_obj = BRISQUE()
