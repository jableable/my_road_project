import collections
import osmnx as ox
import shapely
from shapely.geometry import box as sgbox
from shapely.ops import (
    unary_union,
    polygonize,
    Point,
    MultiPoint,
    LineString,
    MultiLineString,
    Polygon
)
import matplotlib.pyplot as plt
import numpy as np
import utm
import cv2
from pyproj import Transformer
from imutils import opencv2matplotlib
import timeit

start = timeit.default_timer()

#checks a list of linestrings if there are duplicates in the form of reversed edges
def check_for_reverse(linestrings):
    final_linestrings = []
    for i, line in enumerate(linestrings):
        if not any(
            LineString.reverse(line) == linestring for linestring in linestrings[:i]
        ):
            final_linestrings.append(line)
    return final_linestrings


#calculates intersections of list linestrings (not including self-intersections)
def get_intersections(lines):
    point_intersections = []
    line_intersections = []
    for i, line1 in enumerate(lines):
        for line2 in lines[i + 1 :]:
            intersection = line1.intersection(line2)
            if isinstance(intersection, LineString):
                line_intersections.append(intersection)
            elif isinstance(intersection, Point):
                point_intersections.append(intersection)
            elif isinstance(intersection, MultiPoint):
                point_intersections.extend(intersection.geoms)
    return point_intersections, line_intersections


#make a shapely.polygon to feed into OSMnx graph_from_polygon 
#step = 764.37037 intended for 640px x 640px Google Maps API images
def make_polygon_for_ox(lat, lng, step = 764.37037):
    #make the bounding polygon with vertices in DD
    flat_transformer = Transformer.from_crs(4326,3857)  #go from DD to mercator projection
    coord_in_merc = flat_transformer.transform(lat,lng) 
    SW = coord_in_merc[0]-step,coord_in_merc[1]-step
    SE = coord_in_merc[0]+step,coord_in_merc[1]-step
    NW = coord_in_merc[0]-step,coord_in_merc[1]+step
    NE = coord_in_merc[0]+step,coord_in_merc[1]+step
    #when switching back, need to swap lat/lng
    curved_transformer = Transformer.from_crs(3857,4326)    #go from mercator projection back to DD
    gmaps_SW = curved_transformer.transform(SW[0],SW[1])
    gmaps_SW = [gmaps_SW[1-i] for i in range(2)]
    gmaps_SE = curved_transformer.transform(SE[0],SE[1])
    gmaps_SE = [gmaps_SE[1-i] for i in range(2)]
    gmaps_NW = curved_transformer.transform(NW[0],NW[1])
    gmaps_NW = [gmaps_NW[1-i] for i in range(2)]
    gmaps_NE = curved_transformer.transform(NE[0],NE[1])
    gmaps_NE = [gmaps_NE[1-i] for i in range(2)]
    gmaps_polygon = Polygon([gmaps_SW,gmaps_NW,gmaps_NE,gmaps_SE])
    return gmaps_polygon


#make expanded shapely.polygon for bug testing (certain edges are being forgotten)
#  big_step = 2000 to catch every edge?
def make_expanded_polygon_for_ox(lat,lng, big_step = 2000):
    #make the bounding polygon with vertices in DD
    flat_transformer = Transformer.from_crs(4326,3857)  #go from DD to mercator projection
    coord_in_merc = flat_transformer.transform(lat,lng)

    SW = coord_in_merc[0]-big_step,coord_in_merc[1]-big_step
    SE = coord_in_merc[0]+big_step,coord_in_merc[1]-big_step
    NW = coord_in_merc[0]-big_step,coord_in_merc[1]+big_step
    NE = coord_in_merc[0]+big_step,coord_in_merc[1]+big_step
    #when switching back, need to swap lat/lng
    curved_transformer = Transformer.from_crs(3857,4326)    #go from mercator projection back to DD
    gmaps_SW = curved_transformer.transform(SW[0],SW[1])
    gmaps_SW = [gmaps_SW[1-i] for i in range(2)]
    gmaps_SE = curved_transformer.transform(SE[0],SE[1])
    gmaps_SE = [gmaps_SE[1-i] for i in range(2)]
    gmaps_NW = curved_transformer.transform(NW[0],NW[1])
    gmaps_NW = [gmaps_NW[1-i] for i in range(2)]
    gmaps_NE = curved_transformer.transform(NE[0],NE[1])
    gmaps_NE = [gmaps_NE[1-i] for i in range(2)]
    gmaps_polygon = Polygon([gmaps_SW,gmaps_NW,gmaps_NE,gmaps_SE])
    return gmaps_polygon


#make the red bounding polygon in UTM (need to perform affine transformation from gmaps_polygon to here)
def make_viewing_window(gmaps_polygon):
    old_poly = list(gmaps_polygon.exterior.coords)
    utm_SW = utm.from_latlon(old_poly[0][1],old_poly[0][0])[0:2]
    utm_NW = utm.from_latlon(old_poly[1][1],old_poly[1][0])[0:2]
    utm_NE = utm.from_latlon(old_poly[2][1],old_poly[2][0])[0:2]
    utm_SE = utm.from_latlon(old_poly[3][1],old_poly[3][0])[0:2]
    return utm_SW, utm_NW, utm_NE, utm_SE

def shift_to_origin(SW,NW,NE,SE):
      #shift box to coordinate axes x=0 and y=0 and store vertices as "shifted_points"
    xshift = min(SW[0],NW[0])
    yshift = min(SW[1],SE[1])
    shifted_points = [[SW[0]-xshift,SW[1]-yshift],
                  [NW[0]-xshift,NW[1]-yshift],
                  [NE[0]-xshift,NE[1]-yshift],
                  [SE[0]-xshift,SE[1]-yshift]
                  ]
    return shifted_points,xshift,yshift


#returns number of crossings within 640px X 640px bounding box centered at (lat,lng)
def return_crossings(lat,lng, step = 764.37037, big_step = 2000):   

    #make a graph object if possible (whose edges are contained within gmaps_polygon)
    try:
        G = ox.project_graph(ox.graph_from_polygon(
            polygon=make_expanded_polygon_for_ox(lat,lng, big_step=big_step),
            network_type="drive",
            truncate_by_edge=True,
            retain_all=True,
        )
        )
    except Exception as e:
        print("error! read:",e)
        return 0
    
    #extract edges from graph
    edges = ox.graph_to_gdfs(G, nodes=False)

    #prevent calculation of edge intersections if too many edges
    if len(edges)>1100:     #1100 seems about right
        print(f"that's a lot of edges...{len(edges)} in fact!")
        return "too_many_edges"
    
    multi_line = edges.geometry.values

    #create polygon in UTM to show in red later
    viewing_polygon = make_viewing_window(make_polygon_for_ox(lat,lng,step))     

    #make polygon to check if intersections fall within
    polygon_unshifted = Polygon(viewing_polygon) 

    # Build cleaned final_linestrings with reverse duplicates removed
    final_linestrings = check_for_reverse(multi_line)

    # Initialize list of endpoints of linestrings
    endpoints = [
        point for line in final_linestrings for point in shapely.boundary(line).geoms
    ]
    endpoints = np.unique(
        [shapely.get_coordinates(point)[0] for point in endpoints], axis=0
    )

    # Get all intersections (including nodes)
    intersections = get_intersections(final_linestrings)[0]
    if len(intersections)==0:
        return 0
    
    final_intersections = [shapely.get_coordinates(point)[0] for point in intersections]

    for line in final_linestrings:
        mls = unary_union(line)
        if isinstance(mls, MultiLineString):
            coords_list = [
                coord
                for non_intersecting_ls in mls.geoms
                for coord in non_intersecting_ls.coords
            ]
            self_intersecting_points = [
                coord
                for coord, count in collections.Counter(coords_list).items()
                if count > 1
            ]
            final_intersections.extend(self_intersecting_points)

    
    # Find crossings (intersections that are not endpoints)
    crossings = [point for point in final_intersections if point not in endpoints]
    final_crossings=[]             
    for crossing in crossings:
        pt_crossing = Point(crossing)
        if polygon_unshifted.contains(pt_crossing):
            final_crossings.append(pt_crossing)
    return polygon_unshifted,final_linestrings,final_crossings,crossings



#show the satellite image with edges and vertices
def visualize_map(lat,lng,img_path,polygon_unshifted,final_linestrings,final_crossings,crossings):        

    #create polygon in UTM to show in red later
    viewing_polygon = make_viewing_window(make_polygon_for_ox(lat,lng)) 
    #shift vertices to x- and y- axes
    shifted_object = shift_to_origin(viewing_polygon[0], viewing_polygon[1], viewing_polygon[2],viewing_polygon[3])       
    xmax = max(shifted_object[0][2][0],shifted_object[0][3][0])   
    ymax = max(shifted_object[0][1][1],shifted_object[0][2][1])                               
    shifted_points, xshift, yshift = shifted_object[0:3]
    #make red polygon out of shifted points to be displayed in plot
    red_polygon= plt.Polygon(shifted_points,  fill=None, edgecolor='r') 

    #Shift all linestrings to x-axis and y-axis
    shifted_final_linestrings = []
    for line in final_linestrings:
        shifted_line=[]
        for i in range(len(line.xy[0])):
            shifted_line.append([line.coords[i][0]-xshift,line.coords[i][1]-yshift])
        line = LineString(shifted_line)
        shifted_final_linestrings.append(line)

    #shift all intersections
    shifted_final_crossings=[]   
    for crossing in crossings:
        pt_crossing = Point(crossing)
        if polygon_unshifted.contains(pt_crossing):
            shifted_crossing = (crossing[0]-xshift,crossing[1]-yshift)
            shifted_final_crossings.append(Point(shifted_crossing))

    #open and flip the satellite image (not sure why image needs to be flipped)
    img = cv2.imread(img_path)
    img = cv2.flip(img,0)

    #form list of input and output points for affine transformation
    pts1 = np.float32([[0, 640],
                        [640, 640], [640, 0]])
    pts2 = np.float32([shifted_points[1],shifted_points[2],shifted_points[3]])

    #get matrix of affine transformation and apply it to image
    matrix = cv2.getAffineTransform(pts1, pts2)   
    result = cv2.warpAffine(img, matrix, (int(xmax), int(ymax)))

    # Plot the satellite image, graph edges, black crossing vertices, and red bounding box
    fig, ax = plt.subplots()
    #ax.get_xaxis().set_visible(False)
    #ax.get_yaxis().set_visible(False)
    ax.set_xlim(-1,xmax+1)
    ax.set_ylim(-1,ymax+1)
    ax.imshow(opencv2matplotlib(result))
    for line in shifted_final_linestrings:
        ax.plot(line.xy[0], line.xy[1], zorder=0)
    
    ax.add_patch(red_polygon)

    for point in crossings:
        ax.scatter(point[0], point[1], s=2, c="black", zorder=1)

    for point in shifted_final_crossings:
        ax.scatter(shapely.get_coordinates(point)[0][0], shapely.get_coordinates(point)[0][1], s=2, c="black", zorder=1)        

    print(f"I see {len(final_crossings)} crossings!")

    return xshift, yshift, result

#enter desired lat/lng below to see graph/intersections overlaid on satellite image
if __name__ == "__main__":
    lat, lng = 39.10875730183322, -86.55947381472457
    object = return_crossings(lat, lng)
    if type(object) is str:
        print("we're not graphing that")
    if type(object) is tuple:
        poly, edges, crossings, crossings2 = return_crossings(lat, lng)
        visualize_map(lat, lng,
            img_path="./assets/images/bloomington_sat_map.png",
            polygon_unshifted = poly,
            final_linestrings=edges,
            final_crossings=crossings,crossings=crossings2)
        plt.show()
    if type(object) is int:
        print("we could graph that, but there are no crossings")
    