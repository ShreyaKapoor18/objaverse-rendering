import h5py

def get_group_structure(file_path):
    group_structure = set()

    with h5py.File(file_path, 'r') as file:
        file.visit(group_structure.add)

    return group_structure

# Replace with the paths to your HDF5 files
file_path_1 = 'original_2023-11-17_20-09-25.hdf5'
file_path_2 = 'original_2023-11-22_16-57-00.hdf5'

# Get the structure of groups in both files
structure_1 = get_group_structure(file_path_1)
structure_2 = get_group_structure(file_path_2)

# Check for overlapping groups
overlapping_groups = structure_1.intersection(structure_2)
num_overlapping_groups = len(overlapping_groups)
print(num_overlapping_groups)
if overlapping_groups:
    print("Overlapping directories/groups found:")
    for group in overlapping_groups:
        print(group)
else:
    print("No overlapping directories/groups found.")

