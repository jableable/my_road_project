import sys
sys.path.append('..')
from verifying_crossing_counter import return_crossings
import os
from pathlib import Path 
import ast

file = 'asia'
with open('../assets/coordinates/too many edges/'+file+'.txt', 'r') as input:
    coords = input.read().replace('\n', '')
    coords = ast.literal_eval(coords)


path = Path('../assets/images/dataset/labeled/')

visible_files = [
    file for file in path.iterdir() if not file.name.startswith(".")
]

directory = '../assets/images/dataset/labeled/'
num_files = len(visible_files)
counter = 0
for file in visible_files:
    if file.name.endswith('.png'):
        try:
            orig_filename = file.name
            orig_filename2 = orig_filename.strip(".png").split(",")
            orig_cross_num, lat, lng = orig_filename2[0], orig_filename2[1], orig_filename2[2]
            lat = float(lat.replace("'",""))
            lng = float(lng.replace("'",""))
            print(lat,lng)
            if (lat, lng) in coords:
                print("found a big one")
                poly, edges, crossings, crossings2 = return_crossings(lat, lng)
                cross_num = len(crossings)
                new_filename=directory+str(cross_num)+","+str(lat)+","+str(lng)+".png"
                os.rename(file, new_filename)
                counter += 1
                print("old crossing number:",str(orig_cross_num)," new crossing number:",str(cross_num))
                print(counter,"files down, ",num_files - counter,"to go!")
        except Exception as e:
            print("error! see:",e)



            



