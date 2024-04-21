import os
import base64
import glob
from os.path import join

folder_names = os.listdir('/Users/shreya/Documents/GitHub/objaverse-rendering/jsons')

for directory in folder_names:
    if '.' not in directory:
        print(directory)
        # Specify the directory you want to list the folders for
        directory_path = f"/Users/shreya/Documents/GitHub/objaverse-rendering/jsons/{directory}/"
        #print(directory_path)
        # Define the dataset name
        dataset_name = directory_path.split('/')[-2]
        #print(dataset_name)

        # Create HTML content to embed multiple images
        html_content = f"""<!DOCTYPE html>
        <html>
        <head>
            <title>{dataset_name}</title>
        </head>
        <body>
            <h1>{dataset_name}</h1>
            <table>
        """

        # Loop through all the image files in the first 50 folders
        i = 0
        
        for folder in glob.glob(join(directory_path, '*')):
            i += 1
            if i > 50:
                break

            # Create a new row for each folder
            html_content += f"<tr><td><h2>Folder: {os.path.basename(folder)}</h2></td></tr>"

            # Initialize a count to track the number of images in the current row
            image_count = 0

            # Embed each image in the HTML content
            for image_file in os.listdir(folder):
                # Get the full path to the image file
                full_image_path = os.path.join(folder, image_file)

                # Read and encode the image to base64
                with open(full_image_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode("utf-8")

                # Embed each image in a cell of the table
                html_content += f"""<td><figure><img src="data:image/jpeg;base64,{base64_image}" alt="{full_image_path}"><br><br><figcaption>{os.path.basename(folder)}</figcaption></figure></td>"""

                # Increment the image count
                image_count += 1

                # Check if 12 images have been added to the current row
                if image_count == 12:
                    # Close the row and start a new one
                    html_content += "</tr><tr>"
                    image_count = 0

            # Close the row for the current folder
            html_content += "</tr>"


    directory_path_2 = f"/Users/shreya/Documents/GitHub/objaverse-rendering/{directory}/original"
    #print(directory_path_2)
    # Define the dataset name
    for folder in glob.glob(join(directory_path_2, '*')):
        dataset_name = folder.split('/')[-2] + '_original'
        #print(dataset_name)
        html_content += f"<tr><td><h2>Folder: {os.path.basename(folder)} Original</h2></td></tr>"

        # Initialize a count to track the number of images in the current row
        image_count = 0

        # Embed each image in the HTML content
        for image_file in os.listdir(folder):
            # Get the full path to the image file
            full_image_path = os.path.join(folder, image_file)

            # Read and encode the image to base64
            with open(full_image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")

            # Embed each image in a cell of the table
            html_content += f"""<td><img src="data:image/jpeg;base64,{base64_image}" alt="{full_image_path}"><br><br></td>"""

            # Increment the image count
            image_count += 1

            # Check if 12 images have been added to the current row
            if image_count == 12:
                # Close the row and start a new one
                html_content += "</tr><tr>"
                image_count = 0

        # Close the row for the current folder
        html_content += "</tr>"
    
    # Close the HTML content
        html_content += f"""</table></body></html>"""
    #print(' Name of the dataset', dataset_name)
    # Save the HTML file with embedded images and additional content
        with open(os.path.join(f"{dataset_name}.html"), "w") as html_file:
            html_file.write(html_content)
        #print("HTML file with embedded images and additional content has been created.")

# Assuming len(folder_names) is the number of folders you have

print('***'*20)             
html_table = "<table>"

# Assuming len(folder_names) is the number of folders you have
num_folders = len(folder_names)
print(folder_names)
# Print folder names as headers
html_table += "<tr>"
folder_names_out = ['ambient_ill', 'less_variation', 'no_variation', 'wo_all', 'z_axis']
for folder in folder_names_out:
    html_table += f"<th>{folder}</th>"
html_table += "</tr>" # first rqw of the table is done
file_paths = []
# Iterate over folders
total = 0
for j in range(num_folders):
    folder = folder_names[j]
    total+=1
    if '.' not in folder:
        folder_path = f"/Users/shreya/Documents/GitHub/objaverse-rendering/jsons/{folder}/"
        
        # Get all file paths within the folder
        all_file_paths = [os.path.join(folder_path, id, image)
                        for id in os.listdir(folder_path)
                        for image in os.listdir(os.path.join(folder_path, id))]
        file_paths.append(all_file_paths)
max_images = max([len(file_paths[j]) for j in range(len(file_paths))])
print('***'*20)
print(max_images)    
for i in range(max_images):
    html_table += "<tr>"
    for j in range(len(file_paths)):
        print(len(file_paths))
        # Get the image path
        try:
            image_path = file_paths[j][i]
        except IndexError:
            image_path = '/Users/shreya/Documents/GitHub/objaverse-rendering/imgres.html'
        #print(image_path)
        # Read and encode the image to base64
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            # Embed each image in a cell of the table
            html_table += f"""<td><figure><img src="data:image/jpeg;base64,{base64_image}" alt="{image_path}"><center><figcaption><b>{folder_names_out[j//2]}</b></figcaption></center></figure><br><br></td>"""
    html_table += "</tr>"   
html_table += "</table>"
#print(html_table)
# Close the HTML table
with open("compare_all.html", "w") as html_file:
    html_file.write(html_table)
    print("HTML file with embedded images and additional content has been created.")
#rflow.com/questions/3715493/encoding-an-image-file-with-base64 
    
    