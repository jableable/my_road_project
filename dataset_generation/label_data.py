import ast
import sys
sys.path.append('..')
from verifying_crossing_counter import return_crossings
import io
from PIL import Image
import urllib.request
from time import sleep
import numpy as np


#use pregenerated coords
#file = 'euro_coords_cleaned'
#with open('../assets/coordinates/clean/'+file+'.txt', 'r') as input:
    #coords = input.read().replace('\n', '')
    #coords = ast.literal_eval(coords)

#generate random coords
coords=[]
for i in range (2400):
    coords.append((np.random.uniform(16.5,48),np.random.uniform(73.5,82)))


#get img from Static Maps API and label it according to crossing_counter
for i, coord in enumerate(coords):
    try:
        filename=str(len(return_crossings(coords[i][0],coords[i][1])[2]))+","+str(coords[i][0])+","+str(coords[i][1])+".png"
        url = "https://maps.googleapis.com/maps/api/staticmap?center="+str(coords[i][0])+","+str(coords[i][1])+"&zoom=16&size=640x640&maptype=satellite&key=YOUR_API_KEY_HERE"
        buffer = io.BytesIO(urllib.request.urlopen(url).read())
        img = Image.open(buffer)
        img.save("../assets/images/dataset/labeled/"+filename, quality=100)      
        i+=1      
        print("saved image",i)
        sleep(.5)
    except Exception as e:
        print("error at",i, "! look:",e)
        sleep(.5)





