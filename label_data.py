import ast
from crossing_counter import return_crossings
import io
from PIL import Image
import urllib.request
import cv2
from time import sleep
import simplejson as json
import pprint
import requests

#separate string in .txt file into coordinate pairs
with open('C:/Users/Jared/Desktop/combined_coords.txt', 'r') as file:
    coords = file.read().replace('\n', '')
    coords = ast.literal_eval(coords)


#check for duplicates
    #for i,pair1 in enumerate(coords):
        #for j in range(i+1,len(coords)-i):
            #if abs(pair1[0] - coords[j][0])<=.001:    #check if x-values are close
                #if .000<=abs(pair1[1] - coords[j][1])<=.002:  #check if y-values are close
                    #print(f"our close points are: {pair1} and {coords[j]}")

for coord in coords:
    i=100
    while i<500: 
        try:
            url = "https://maps.googleapis.com/maps/api/staticmap?center="+str(coords[i][0])+","+str(coords[i][1])+"&zoom=16&size=640x640&maptype=satellite&key=AIzaSyCzzVb_qf0TQgLw3K2y5EE6geyzE6KzQuA"
            buffer = io.BytesIO(urllib.request.urlopen(url).read())
            img = Image.open(buffer)
            filename=str(len(return_crossings(coords[i][0],coords[i][1])[3]))+","+str(coords[i][0])+","+str(coords[i][1])+".png"
            img.save("./assets/images/dataset/"+filename, quality=100)
            i+=1
            print("saved image",i)
            sleep(1)
        except Exception as e:
            print("error! look:",e)
            sleep(1)



