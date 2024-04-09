from crossing_counter import return_crossings
import numpy as np
from pyproj import Transformer

#for bounding box: find upper and lower lat/lng bounds based on step; steps are distances in mercator projection
def get_bounds(lat, lng, step):
    #make the bounding polygon with vertices in DD
    flat_transformer = Transformer.from_crs(4326,3857)  #go from DD to mercator projection
    coord_in_merc = flat_transformer.transform(lat,lng) 
    lower_lat_bound = coord_in_merc[0]-step
    upper_lat_bound = coord_in_merc[0]+step
    lower_lng_bound = coord_in_merc[1]-step
    upper_lng_bound = coord_in_merc[1]+step
    #when switching back, need to swap lat/lng
    curved_transformer = Transformer.from_crs(3857,4326)    #go from mercator projection back to DD
    SW_point = curved_transformer.transform(lower_lat_bound,lower_lng_bound)
    NE_point = curved_transformer.transform(upper_lat_bound,upper_lng_bound)
    return SW_point[0],NE_point[0],SW_point[1],NE_point[1]


#initialize list of coordinates to be filled
list_of_crossings = []

#city step is largest and acts as a large first pass 
#zoom1 step is smaller and acts as more refined second pass
#zoom2 step is smallest and acts as most refined final pass (this step corresponds to dataset images)
city_step = 3000
zoom1_step = 1500
zoom2_step = 764.37037

#output stops after accumulating 100 coordinates
while len(list_of_crossings)<=500:
    #randomly pick from a rectangular subset of USA
    lat = np.random.uniform(32.5,48)  #(-90,90)
    lon = np.random.uniform(-117,-81.5) #(-180,180)
    print(f"checking for a new city at {lat,lon}")
    #output of return crossings is either a string, tuple, or integer
    goal = return_crossings(lat,lon,step = city_step, big_step=4000)

    #type(goal) is string when large windows makes it unfeasible to calculate edge intersections
    if type(goal) is str:
        print("too many edges!")
        #zoom in from city_step to zoom1_step to reduce number of edges
        zoom1_crossings = 0
        counter1 = 0
        #search within city_step box using smaller, random zoom1_step boxes
        #search concludes when crossing is located or 10 searches have been performed (there may be no crossing)
        (lower_lat_bound, upper_lat_bound, lower_lng_bound, upper_lng_bound) = get_bounds(lat, lon, city_step)
        while zoom1_crossings <= 1 and counter1<=10:            
            zoom1_lat = np.random.uniform(lower_lat_bound, upper_lat_bound)
            zoom1_lon = np.random.uniform(lower_lng_bound, upper_lng_bound)
            zoom1_crossings = return_crossings(zoom1_lat,zoom1_lon,step = zoom1_step, big_step = 2000)
            counter1 += 1

            if type(zoom1_crossings) is str:
                print("too many edges after zooming in!!")
                zoom2_crossings = 0
                counter2 = 0
                (lower_lat_bound, upper_lat_bound, lower_lng_bound, upper_lng_bound) = get_bounds(zoom1_lat, zoom1_lon, zoom1_step)
                while zoom2_crossings <= 1 and counter2<=15:                    
                    zoom2_lat = np.random.uniform(lower_lat_bound, upper_lat_bound)
                    zoom2_lon = np.random.uniform(lower_lng_bound, upper_lng_bound)
                    zoom2_crossings = return_crossings(zoom2_lat,zoom2_lon,step = zoom2_step, big_step = 2000)
                    counter2 += 1
                    if type(zoom2_crossings) is str:
                        print("too many edges after zooming in again!!!") 
                        break   
                    if type(zoom2_crossings) is tuple:
                        zoom2_crossings = len(zoom2_crossings[2])
                if type(zoom2_crossings) is int:
                    if zoom2_crossings >= 1:
                        print("found a zoom2 crossing! appending...")
                        zoom2_crossings += zoom2_crossings
                        list_of_crossings.append((zoom2_lat,zoom2_lon))
                break  

            if type(zoom1_crossings) is tuple:
                zoom1_crossings = len(zoom1_crossings[2])

            if type(zoom1_crossings) is int:
                if zoom1_crossings >= 1:
                    print("found a zoom1 crossing; looking for a zoom2 crossing")
                    zoom2_crossings = 0
                    counter2 = 0
                    (lower_lat_bound, upper_lat_bound, lower_lng_bound, upper_lng_bound) = get_bounds(zoom1_lat, zoom1_lon, zoom1_step)
                    while zoom2_crossings <= 1 and counter2<=15:                        
                        zoom2_lat = np.random.uniform(lower_lat_bound, upper_lat_bound)
                        zoom2_lon = np.random.uniform(lower_lng_bound, upper_lng_bound)
                        zoom2_crossings = return_crossings(zoom2_lat,zoom2_lon,step = zoom2_step,big_step = 2000)
                        counter2 += 1
                        if type(zoom2_crossings) is tuple:
                            zoom2_crossings = len(zoom2_crossings[2])
                        #deal with rare (?) edge case of too many edges when zoomed in, but not when zoomed out
                        if type(zoom2_crossings) is str:
                            zoom2_crossings=0
                        if zoom2_crossings >= 1:
                            print("found a zoom2 crossing! appending...")
                            zoom2_crossings += zoom2_crossings
                            list_of_crossings.append((zoom2_lat,zoom2_lon))                    
                            print(f"so far we have {len(list_of_crossings)} coordinate pairs, and the list is {list_of_crossings}")
        continue

    #type(goal) is tuple when crossings have been calculated; goal[2] has desired list of crossings
    if type(goal) is tuple:
        goal = len(goal[2])

    #type(goal) is int when crossings have been calculated
    #most coordinates would give goal=0
    if type(goal) is int:
        if goal >= 1:
            print("found a zoom0 crossing; looking for a zoom1 crossing")
            zoom1_crossings = 0
            counter1 = 0
            (lower_lat_bound, upper_lat_bound, lower_lng_bound, upper_lng_bound) = get_bounds(lat, lon, city_step)
            while zoom1_crossings <= 1 and counter1<=20:                
                zoom1_lat = np.random.uniform(lower_lat_bound, upper_lat_bound)
                zoom1_lon = np.random.uniform(lower_lng_bound, upper_lng_bound)
                zoom1_crossings = return_crossings(zoom1_lat,zoom1_lon,step = zoom1_step,big_step = 2000)
                if type(zoom1_crossings) is tuple:
                    zoom1_crossings = len(zoom1_crossings[2]) 
                counter1 += 1
                #deal with rare (?) edge case of too many edges when zoomed in, but not when zoomed out
                if type(zoom1_crossings) is str:
                    zoom1_crossings=0
            if zoom1_crossings >= 1:
                print("found a zoom1 crossing; looking for a zoom2 crossing")
                zoom2_crossings = 0
                counter2=0
                (lower_lat_bound, upper_lat_bound, lower_lng_bound, upper_lng_bound) = get_bounds(zoom1_lat, zoom1_lon, zoom1_step)
                while zoom2_crossings <= 1 and counter2<=20:
                    zoom2_lat = np.random.uniform(lower_lat_bound, upper_lat_bound)
                    zoom2_lon = np.random.uniform(lower_lng_bound, upper_lng_bound)
                    zoom2_crossings = return_crossings(zoom2_lat,zoom2_lon,step = zoom2_step,big_step = 2000)
                    if type(zoom2_crossings) is tuple:
                        zoom2_crossings = len(zoom2_crossings[2]) 
                    if type(zoom2_crossings) is str:
                        zoom2_crossings = 0
                    counter2 += 1 
                if zoom2_crossings >= 1:
                    print("found a zoom2 crossing! appending...")
                    zoom2_crossings += zoom2_crossings
                    list_of_crossings.append((zoom2_lat,zoom2_lon))

                print(f"so far we have {len(list_of_crossings)} coordinate pairs, and the list is {list_of_crossings}")
                

#save list of crossings to text file in same directory
filename = 'output.txt'
outfile = open(filename, 'w')
outfile.writelines([str(i)+"," for i in list_of_crossings])
outfile.close()