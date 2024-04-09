import sys
sys.path.append('..')
from crossing_counter import return_crossings, visualize_map
import shapely
from shapely.geometry import box as sgbox
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

#crop satellite image to only show area surrounding crossings
def save_cropped_image(orig_filename,crossings,xshift,yshift,transformed_img):
    boxes=[]
    # make box around each crossing
    for i, crossing in enumerate(crossings):
        center = shapely.get_coordinates(crossing)[0]
        box_xstep = 90
        box_ystep = 90
        minx = center[0]-box_xstep
        miny = center[1]-box_ystep
        maxx = center[0]+box_xstep
        maxy = center[1]+box_ystep 
        cross_box = sgbox(minx,miny,maxx, maxy)
        boxes.append(cross_box)
    shifted_contours=[]
    if len(boxes)>0:
        multi_poly = shapely.unary_union(boxes)
        if multi_poly.geom_type == 'MultiPolygon':
            for poly in multi_poly.geoms:
                x,y=poly.exterior.xy
                x=[int(a-xshift) for a in x]
                y=[int(a-yshift) for a in y]
                shifted_contours.append(np.array(list(zip(x,y))))
        elif multi_poly.geom_type == 'Polygon':
            x,y=multi_poly.exterior.xy
            x=[int(a-xshift) for a in x]
            y=[int(a-yshift) for a in y]
            shifted_contours.append(np.array(list(zip(x,y))))
        else:
            print("what?")

    fill_color = [255, 255, 255] # any BGR color value to fill with
    mask_value = 255            # 1 channel white (can be any non-zero uint8 value)

    # our stencil - some `mask_value` contours on black (zeros) background, 
    # the image has same height and width as `img`, but only 1 color channel
    stencil  = np.zeros(transformed_img.shape[:-1]).astype(np.uint8)
    cv2.fillPoly(stencil, shifted_contours, mask_value)

    sel      = stencil != mask_value # select everything that is not mask_value
    transformed_img[sel] = fill_color            # and fill it with fill_color

    transformed_img = cv2.flip(transformed_img,0)
    cv2.imwrite("../assets/images/dataset/cropped/"+orig_filename, transformed_img)



directory = '../assets/images/dataset'
for file in os.listdir(directory):
    orig_filename = file
    if orig_filename[0] != "0":
        filename = file.strip(".png").split(",")
        print(filename)
        cross_num, lat, lng = filename[0], filename[1], filename[2]
        lat = float(lat.replace("'",""))
        lng = float(lng.replace("'",""))
        print(lat,lng)
        poly, edges, crossings, crossings2 = return_crossings(lat, lng)

        img_path="../assets/images/dataset/"+str(cross_num)+","+str(lat)+","+str(lng)+".png"

        xshift, yshift, transformed_img = visualize_map(lat, lng, img_path,
                polygon_unshifted=poly,
                final_linestrings=edges,
                final_crossings=crossings,crossings=crossings2)
        
        save_cropped_image(orig_filename,crossings,xshift,yshift,transformed_img)
        plt.clf()
            


    

