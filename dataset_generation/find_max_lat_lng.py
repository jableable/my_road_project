import ast
import numpy as np

#extract the maximum latitude and longitude from a txt file which is a list of coordinate pairs (lat,lng)
file = '1032_europe_coords'
#separate string from get_random_coordinates.py .txt file into coordinate pairs
with open('../assets/coordinates/unclean/'+file+'.txt', 'r') as input:
    coords = input.read().replace('\n', '')
    coords = ast.literal_eval(coords)
    coords = list(set(coords))
    xvalues = []
    yvalues = []
    for coord in coords:
        xvalues.append(coord[0])
        yvalues.append(coord[1])

    print("max x-value is ",max(xvalues), "and the min x-value is",min(xvalues))

    print("max y-value is ",max(yvalues), "and the min y-value is",min(yvalues))





