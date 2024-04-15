import sys
sys.path.append('..')
from verifying_crossing_counter import return_crossings, visualize_map
import shapely
from shapely.geometry import box as sgbox
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

img_path = '../assets/images/dataset/labeled/usa_combined/1/9,34.82321117393417,-92.34573404411337.png'

img = cv2.imread(img_path)
M = img.shape[0]//4
N = img.shape[1]//4
tiles = [img[x:x+M,y:y+N] for x in range(0,img.shape[0],M) for y in range(0,img.shape[1],N)]

# show the image, provide window name first
cv2.imshow('image window', tiles[15])
# add wait key. window waits until user presses a key
cv2.waitKey(0)
# and finally destroy/close all open windows
cv2.destroyAllWindows()
