import ast
import sys
sys.path.append('..')
from time import sleep
import os


list_of_coords = []

location = "C:/Users/Jared/Documents/GitHub/my_road_project/assets/images/dataset/labeled/"

files = os.listdir("../assets/images/dataset/labeled/totally random coords usa")
print(len(files))
for file in files:
    file = file.replace(".png","")
    file = file.split(",")
    file_coords = float(file[1]),float(file[2])
    list_of_coords.append(file_coords)

#save list of crossings to text file in same directory
filename = 'image_coords.txt'
outfile = open(filename, 'w')
outfile.writelines([str(i)+"," for i in list_of_coords])
outfile.close()


    
    







