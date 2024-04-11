import ast
import sys
sys.path.append('..')
from crossing_counter import return_crossings
import io
from PIL import Image
import urllib.request
from time import sleep

file = 'usa_coords_cleaned'

with open('../assets/coordinates/clean/'+file+'.txt', 'r') as input:
    coords = input.read().replace('\n', '')
    coords = ast.literal_eval(coords)

for i, coord in enumerate(coords):
    try:
        url = "https://maps.googleapis.com/maps/api/staticmap?center="+str(coords[i][0])+","+str(coords[i][1])+"&zoom=16&size=640x640&maptype=satellite&key=AIzaSyCzzVb_qf0TQgLw3K2y5EE6geyzE6KzQuA"
        buffer = io.BytesIO(urllib.request.urlopen(url).read())
        img = Image.open(buffer)
        filename=str(len(return_crossings(coords[i][0],coords[i][1])[2]))+","+str(coords[i][0])+","+str(coords[i][1])+".png"
        img.save("../assets/images/dataset/labeled/"+filename, quality=100)      
        i+=1      
        print("saved image",i)
        sleep(1)
    except Exception as e:
        print("error at",i, "! look:",e)
        sleep(1)





