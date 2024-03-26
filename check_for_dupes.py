import ast

#check for duplicates
with open('C:/Users/Jared/Desktop/combined_coords.txt', 'r') as file:
    data = file.read().replace('\n', '')
    data = ast.literal_eval(data)

    for i,pair1 in enumerate(data):
        for j in range(i+1,len(data)-i):
            if abs(pair1[0] - data[j][0])<=.001:
                #print(f"x coords are close!: we got {pair1[0] - data[j][0]}")
                if .000<=abs(pair1[1] - data[j][1])<=.002:
                    #print(f"y coords are close!: we got {pair1[1] - data[j][1]}")
                    print(f"our points are close: {pair1} and {data[j]}")

