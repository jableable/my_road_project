import ast
import sys
sys.path.append('..')
import io
from PIL import Image
import urllib.request
from time import sleep
import os

file = 'usa_coords_cleaned2'

with open('../assets/coordinates/clean/'+file+'.txt', 'r') as input:
    coords = input.read().replace('\n', '')
    coords = ast.literal_eval(coords)
print(len(coords))
unprocessed_coords = []

location = "C:/Users/Jared/Documents/GitHub/my_road_project/assets/images/dataset/labeled/"

files = os.listdir("../assets/images/dataset/labeled")
print(len(files))
for file in files:
    present=0
    for coord in coords:
        end_str = str(coord[0])+","+str(coord[1])+".png"
        if file.endswith(end_str) is True:
            present = 1
            break
    if present == 0:
        unprocessed_coords.append(file)
        path = os.path.join(location, file)
        os.remove(path)
print(len(unprocessed_coords))

os.remove(path)
#for i, coord in enumerate(coords):  
    #present = 0
    #end_str = str(coord[0])+","+str(coord[1])+".png"
    #i=0
    #for file in files:
        #if file.endswith(end_str) is True:
            #present = 1
            #print(end_str, file)
            #break
    #if present == 0:
        #unprocessed_coords.append(coord)

#print(len(unprocessed_coords))

    
    







