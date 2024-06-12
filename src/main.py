import dynamic_programming as dp
import divide_and_conquer as dac
import matplotlib.pyplot as plt

def read_input_from_txt(file_path):
    """
    Reads the input from a txt file and returns the values
    """
    with open(file_path, 'r') as file:
        n = int(file.readline().strip())
        iterations = int(file.readline().strip())
        algorithm = int(file.readline().strip())
        control_points = []
        for _ in range(n):
            x, y = map(float, file.readline().strip().split())
            control_points.append((x, y))
    
    return n, iterations, algorithm, control_points

def plot_shapes(control_points, smooth_points, algorithm):
    with plt.style.context('dark_background'):
        fig, ax = plt.subplots()
        control_x, control_y = zip(*control_points)
        smooth_x, smooth_y = zip(*smooth_points)
         
        # Ensure the smooth shape is closed
        smooth_x = list(smooth_x) + [smooth_x[0]]
        smooth_y = list(smooth_y) + [smooth_y[0]]

        ax.plot(control_x, control_y, 'o--', label='Original Shape', color='cyan', markersize=3)
        ax.plot(smooth_x, smooth_y, 'm-', label='Smooth Border')
        
        ax.set_aspect('equal')
        plt.title(f'Original Shape and Smooth Border using {algorithm}')
        plt.legend()
        plt.legend(loc='upper left')
        plt.show()

def main():
    # Select the input method
    print("Select the input method:")
    print("1. Manual input")
    print("2. Read from a file")
    input_method = int(input("Enter the number of the input method: "))
    if input_method == 1:
        # Take input from the user for the control points
        control_points = []
        n = int(input("\nEnter the number of control points: "))
        if n < 2:
            print("At least 2 control points are required to form a Bezier curve.")
            return
        for i in range(n):
            x, y = map(float, input(f"Enter the x and y coordinates of point {i + 1}: ").split())
            control_points.append((x, y))
        # Take input from the user for the number of iterations
        iterations = int(input("Enter the number of iterations: "))
        if iterations < 0:
            print("At least 0 iteration is required.")
            return
        # Input selection for the algorithm to use
        print("\nSelect the algorithm to use:")
        print("1. Brute Force")
        print("2. Divide and Conquer")
        algorithm = int(input("Enter the number of the algorithm: "))
    elif input_method == 2:
        file_path = input("\nEnter the file path: ")
        file_path = "../test/" + file_path
        n, iterations, algorithm, control_points = read_input_from_txt(file_path)
        if n < 2:
            print("At least 2 control points are required to form a Bezier curve.")
            return
        if iterations < 0:
            print("At least 0 iteration is required.")
            return
    else:
        print("Invalid input. Please enter 1 or 2.")
        return
    distance = 0.5
    if algorithm == 1:
        n_sampled_points = 10
        smooth_points_dp, duration_dp = dp.smooth_polygon_dp(control_points, distance, n_sampled_points)
        plot_shapes(control_points,smooth_points_dp, "Dinamyc Programming")
    elif algorithm == 2:
        smooth_points, duration = dac.smooth_shape_divide_and_conquer(control_points, distance, iterations)
        plot_shapes(control_points, smooth_points, "Divide and Conquer")
    else:
        print("Invalid input. Please enter 1 or 2.")
        return
    
    
    print("\nGoodbye! Hope you enjoyed the bezier curve 💞")
    
if __name__ == "__main__":
    main()