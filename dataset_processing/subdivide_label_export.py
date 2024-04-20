import sys
sys.path.append('..')
from subdivided_crossing_counter import return_crossings, visualize_map
import shapely
from shapely.geometry import box as sgbox
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

directory = '../assets/images/dataset/labeled/usa_combined/1/'

for i,file in enumerate(os.listdir(directory)):
    if i>=522:
        coords = file.replace(".png","")
        coords = coords.split(",")
        lat = coords[1]
        lng = coords[2]

        img_path = directory+file
        img = cv2.imread(img_path)
        M = img.shape[0]//4
        N = img.shape[1]//4
        tiles = [img[x:x+M,y:y+N] for x in range(0,img.shape[0],M) for y in range(0,img.shape[1],N)]

        poly, edges, crossings, crossings2 = return_crossings(lat, lng)

        _,_,_,black_polygons_crossing_counts = visualize_map(lat, lng,
                    img_path=img_path,
                    polygon_unshifted = poly,
                    final_linestrings=edges,
                    final_crossings=crossings,crossings=crossings2)
        plt.clf()
        plt.close()

        numbered_tiles = list(zip(tiles, black_polygons_crossing_counts))

        #export tiles with labels
        for i,tile in enumerate(numbered_tiles):
            img_name = str(black_polygons_crossing_counts[i])+","+str(lat)+","+str(lng)+","+str(i)
            output_path = '../assets/images/dataset/labeled/usa_combined/1/subdivided/'+img_name+'.png'
            cv2.imwrite(output_path,tile[0])



