import h5py
import os
import numpy as np

def add_files_to_dataset(group, directory):
    for category in os.listdir(directory):
        category_path = os.path.join(directory, category)
        print(category_path)
        if os.path.isdir(category_path):
            category_group = group.create_group(category)
            print(category_group)
            for item in os.listdir(category_path):
                item_path = os.path.join(category_path, item)
                if os.path.isfile(item_path):
                    with open(item_path, "rb") as file:
                        image_data = np.fromfile(file, dtype=np.uint8)
                        category_group.create_dataset(item, data=image_data)


repository_path = "meshes_lt_100_original"
hdf5_file_path = "meshes_lt_100_dataset.h5"


with h5py.File(hdf5_file_path, "w") as hdf5_file:
    add_files_to_dataset(hdf5_file, repository_path)

print("Files from repository added to HDF5 dataset.")
