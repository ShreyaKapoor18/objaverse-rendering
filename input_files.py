import glob
import h5py
import os
from os.path import join

def get_folders_starting_with(file_paths, prefix):
    folders = set()

    for file_path in file_paths:
        with h5py.File(file_path, 'r') as file:
            for group in file:
                if group.startswith(prefix):
                    folders.add(group)

    return list(folders)

def combine_folders_starting_with(input_files, output_file, prefix):
    folders_to_copy = get_folders_starting_with(input_files, prefix)

    with h5py.File(output_file, 'w') as output:
        for file_path in input_files:
            with h5py.File(file_path, 'r') as file:
                for group in folders_to_copy:
                    if group in file:
                        file.copy(group, output)

# Pattern matching to retrieve HDF5 files with the 'original_20' prefix
input_files = glob.glob(join(os.getcwd(), 'original_20*.hdf5'))

# Output file to store the combined folders starting with "original_20"
output_file = 'combined_original_20_output.hdf5'  # Replace with the desired output file name

# Prefix to filter folders (groups)
folder_prefix = 'original_20'

combine_folders_starting_with(input_files, output_file, folder_prefix)

