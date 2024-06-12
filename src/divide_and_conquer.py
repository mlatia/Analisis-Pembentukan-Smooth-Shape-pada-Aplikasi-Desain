import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, pi
import matplotlib.image as mpimg
import time
def midpoint(point1, point2):
    return (point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2

def insert_midpoints(arr, midpoints):
    for i in range(len(arr) - 1, 0, -1):
        arr.insert(i, midpoints[i - 1])
    return arr

def bezier(control_points, all_points, iterations):
    if iterations == 0:
        return all_points
    else:
        # Calculate the midpoints
        mid1 = []
        for i in range(1, len(control_points)):
            mid1.append(midpoint(control_points[i-1], control_points[i]))
        all_points.append(mid1)
        # Calculate the midpoints of the midpoints
        mid2 = []
        for i in range(1, len(mid1)):
            mid2.append(midpoint(mid1[i-1], mid1[i]))
        # If it's already the last iteration, add the curve's points to the list and return
        if iterations == 1:
            curve = []
            curve.append(control_points[0])
            curve.extend(mid2)
            curve.append(control_points[-1])
            all_points.append(curve)
            return all_points
        # Insert both midpoints lists as new control points for the next iteration
        new_control_points = []
        new_control_points.append(control_points[0])
        new_control_points.extend(insert_midpoints(mid1, mid2))
        new_control_points.append(control_points[-1])
        # Recursively call the function for the next iteration
        return bezier(new_control_points, all_points, iterations - 1)
    
    
def new_point(point, angle, distance):
    return (point[0] + distance * cos(angle), point[1] + distance * sin(angle))

def smooth_shape_divide_and_conquer(control_points, distance, iteration):
    bezier_points = []
    n = len(control_points)
    start_time = time.time()
    for i in range(n):
        angle1 = pi + np.arctan2(control_points[i][1] - control_points[i-1][1], control_points[i][0] - control_points[i-1][0])
        angle2 = np.arctan2(control_points[(i+1) % n][1] - control_points[i][1], control_points[(i+1) % n][0] - control_points[i][0])
        
        new_point1 = new_point(control_points[i], angle1, distance)
        new_point2 = new_point(control_points[i], angle2, distance)
        
        local_bezier = bezier([new_point1, control_points[i], new_point2], [control_points[i]], iteration)[-1]
        bezier_points.extend(local_bezier)
    end_time = time.time()
    smoothing_duration = end_time - start_time
    print(f"Smoothing duration (DNC): {smoothing_duration:.8f} seconds")
    return bezier_points, smoothing_duration