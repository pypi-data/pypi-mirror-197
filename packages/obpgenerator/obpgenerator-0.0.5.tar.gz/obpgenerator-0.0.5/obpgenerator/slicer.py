import pyvista as pv
import numpy as np
import svgwrite
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches


def find_min_max_z(mesh): #Finds min and max point in the z-direction
      min_value = 0
      max_value = 0
      for point in mesh.points:
            z_value = point[2]
            if z_value < min_value:
               min_value = z_value
            elif z_value > max_value:
               max_value = z_value
      return min_value, max_value

def create_matplot_path(list_layer):
    def find(arr , value):
        for x in range(len(arr)):
            if arr[x] == value:
                return x
    start_points = []
    end_points = []
    for points in list_layer:
        start_points.append(points[0])
        end_points.append(points[1])
    start = start_points[0]
    end = end_points[0]
    start_points.pop(0)
    end_points.pop(0)
    sorted_list =[(start.real,start.imag), (end.real,end.imag)]
    codes = [Path.MOVETO]

    while len(start_points)>0:
        i = find(start_points,end)
        sorted_list.append((end_points[i].real,end_points[i].imag))
        codes.append(Path.LINETO)
        end = end_points[i]
        if type(start_points) is list:
            start_points.pop(i)
            end_points.pop(i)
        else:
            start_points = []
            end_points = []
    codes.append(Path.CLOSEPOLY)
    path = Path(sorted_list, codes)

    return path
        
def calc_layer_coordinates(layer): #Convert a pv polydata layer to an array with coordinates
    layer_connections = layer.lines
    layer_points = layer.points
    new_layer = []
    for i in range(1,len(layer_connections),3):
        pos1 = layer_connections[i]
        pos2 = layer_connections[i+1]
        x_pos1 = layer_points[pos1][0]
        y_pos1 = layer_points[pos1][1]
        pos1 = x_pos1 + y_pos1*1j
        x_pos2 = layer_points[pos2][0]
        y_pos2 = layer_points[pos2][1]
        pos2 = x_pos2 + y_pos2*1j
        new_layer.append((pos1,pos2))
    path = create_matplot_path(new_layer)
    return path

def slice_stl(path, layer_height):
    mesh = pv.read(path)
    min_z, max_z = find_min_max_z(mesh)
    
    slices = []
    z_pos = min_z+layer_height/2
    while z_pos < max_z:
        single_slice = mesh.slice(normal=[0, 0, 1],origin=(0,0,z_pos))
        slice_pos = calc_layer_coordinates(single_slice)
        slices.append(slice_pos)
        z_pos = z_pos + layer_height
    return slices



