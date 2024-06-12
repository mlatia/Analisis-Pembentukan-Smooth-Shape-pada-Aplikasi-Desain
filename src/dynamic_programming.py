import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, pi
import time

def bezier_dp(control_points, n_sampled_points):
    n = len(control_points)
    t_interval = 1.0 / (n_sampled_points - 1)
    output_table = []
    
    for i in range(n_sampled_points):
        t = i * t_interval
        mem_x = [[None for _ in range(n+1)] for _ in range(n)]
        mem_y = [[None for _ in range(n+1)] for _ in range(n)]
        
        def compute_BC_xy(i, n, t):
            if i == n - 1:
                return control_points[i]
            if mem_x[i][n] is not None and mem_y[i][n] is not None:
                return mem_x[i][n], mem_y[i][n]
            left = compute_BC_xy(i, n-1, t)
            right = compute_BC_xy(i+1, n, t)
            mem_x[i][n] = (1 - t) * left[0] + t * right[0]
            mem_y[i][n] = (1 - t) * left[1] + t * right[1]
            return mem_x[i][n], mem_y[i][n]
        
        output_table.append(compute_BC_xy(0, n, t))
    
    return output_table

def new_point(point, angle, distance):
    return point[0] + distance * cos(angle), point[1] + distance * sin(angle)

def smooth_polygon_dp(control_points, distance, n_sampled_points):
    bezier_points = []
    n = len(control_points)
    start_time = time.time()
    for i in range(n):
        angle1 = pi + np.arctan2(control_points[i][1] - control_points[i-1][1], control_points[i][0] - control_points[i-1][0])
        angle2 = np.arctan2(control_points[(i+1) % n][1] - control_points[i][1], control_points[(i+1) % n][0] - control_points[i][0])
        
        new_point1 = new_point(control_points[i], angle1, distance)
        new_point2 = new_point(control_points[i], angle2, distance)
        
        local_bezier = bezier_dp([new_point1, control_points[i], new_point2], n_sampled_points)
        bezier_points.extend(local_bezier)
    end_time = time.time()
    smoothing_duration = end_time - start_time
    print(f"Smoothing duration (DP): {smoothing_duration:.8f} seconds")
    return bezier_points, smoothing_duration