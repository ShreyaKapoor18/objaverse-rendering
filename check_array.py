import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Load the Iris dataset from Plotly Express
data = np.load('results/count_objects.npy')
print('Original Length', len(data))
fig = px.ecdf(data)
fig.show()
print('Setting the threshold of number of geometries to 50')
print(0.93 * len(data), 'Number of objects preserved')

# Create a new figure with a cumulative histogram 

## avoid duplicates

def remove_duplicates(file_path):
    # Read the content of the file and store each line in a list
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove duplicates by converting the list to a set and back to a list
    lines = list(set(lines))

    # Write the unique lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

# Example usage:
file_path = 'results/object_names_50.txt'  # Replace this with the path to your file
remove_duplicates(file_path)