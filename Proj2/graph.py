import matplotlib.pyplot as plt
import math 

def read_data_from_file(file_path):
    x = []
    y = []
    with open(file_path, 'r') as file:
        for line in file:
            values = line.split()
            if len(values) == 4:
                x_value = int(values[0]) * math.log(int(values[0])) * int(values[2])**2
                y_value = float(values[3])
                x.append(x_value)
                y.append(y_value)
    return x, y

# File path to the text file
file_path = './data.txt'

# Read data from file
x, y = read_data_from_file(file_path)

# Create a plot
plt.plot(x, y, marker='o')

# Add title and labels
plt.title('Complexity - Time')
plt.xlabel('Complexity: (V Log(V))')
plt.ylabel('Time: (s)')

# Show the plot
plt.show()