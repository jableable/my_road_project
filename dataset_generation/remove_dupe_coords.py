import ast

file = 'usa_coords'
#separate string from get_random_coordinates.py .txt file into coordinate pairs
with open('../assets/coordinates/clean/'+file+'.txt', 'r') as input:
    coords = input.read().replace('\n', '')
    coords = ast.literal_eval(coords)
    coords = list(set(coords))
    print(len(coords))
    duplicates = []
    #find duplicates (in the sense of "near enough" duplicates)
    for i,pair1 in enumerate(coords):
        for j in range(i+1,len(coords)):
            if abs(pair1[0] - coords[j][0])<=.01:    #check if x-values are close
                if abs(pair1[1] - coords[j][1])<=.01:  #check if y-values are close
                    print(f"our close points are: {pair1} and {coords[j]}")
                    duplicates.append(coords[j])
    duplicates = list(set(duplicates))
    unique_coords = [x for x in coords if x not in duplicates]
    
    print(f"duplicates:{len(duplicates)}, unique coords:{len(unique_coords)}, total coords:{len(coords)}")

with open('../assets/coordinates/clean/'+file+'_cleaned2.txt', 'w') as output:
    print(unique_coords,file=output)

#clean up produced .txt file
with open('../assets/coordinates/clean/'+file+'_cleaned2.txt', 'r') as created:
    coords = created.read().replace("[","").replace("]","")
    coords = coords.replace('\n', '')
    coords = ast.literal_eval(coords)






