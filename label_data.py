import ast
from crossing_counter import return_crossings
import io
from PIL import Image
import urllib.request
from time import sleep

with open('./combined_coords_cleaned.txt', 'r') as input:
    coords = input.read().replace('\n', '')
    coords = ast.literal_eval(coords)

for coord in coords:
    i=0
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




