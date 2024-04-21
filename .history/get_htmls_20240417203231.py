import os
import base64
import glob

# Function to generate HTML content for a single directory
def generate_html(directory_path, dataset_name):
    # Initialize HTML content
    html_content = f"""<!DOCTYPE html>
        <html>
        <head>
            <title>{dataset_name}</title>
        </head>
        <body>
            <h1>{dataset_name}</h1>
            <table>
        """

    # Loop through each folder in the directory
    for folder in glob.glob(os.path.join(directory_path, '*')):
        folder_name = os.path.basename(folder)
        print('the folder name is', folder_name)
        html_content += f"<tr><td><h2>Folder: {folder_name}</h2></td></tr>"
        
        # Initialize image count
        image_count = 0

        # Embed each image in the HTML content
        for image_file in os.listdir(folder):
            full_image_path = os.path.join(folder, image_file)
            with open(full_image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
                html_content += f"""<td><figure><img src="data:image/jpeg;base64,{base64_image}" alt="{full_image_path}"><br><br><figcaption>{image_file}</figcaption></figure></td>"""
                
                # Increment image count
                image_count += 1
                
                # Check if 12 images have been added to the current row
                if image_count == 12:
                    html_content += "</tr><tr>"
                    image_count = 0

        # Close the row for the current folder
        html_content += "</tr>"

    # Close the HTML content
    html_content += "</table></body></html>"
    return html_content

# Define the directory path
base_directory = '/Users/shreya/Documents/GitHub/objaverse-rendering/jsons'
folder_names = [folder for folder in os.listdir(base_directory) if '.' not in folder]

# Generate HTML files for each directory
for directory in folder_names:
    directory_path = os.path.join(base_directory, directory)
    dataset_name = directory_path.split('/')[-1]
    html_content = generate_html(directory_path, dataset_name)
    print(html_content)
    with open(f"{dataset_name}.html", "w") as html_file:
        html_file.write(html_content)

# Generate comparison HTML file
html_table = "<table>"
html_table += "<tr><th>Ambient Ill</th><th>Less Variation</th><th>No Variation</th><th>Wo All</th><th>Z Axis</th></tr>"

# Get file paths for each folder
file_paths = []
for folder in folder_names:
    folder_path = os.path.join(base_directory, folder)
    all_file_paths = [os.path.join(folder_path, id, image) for id in os.listdir(folder_path) for image in os.listdir(os.path.join(folder_path, id))]
    file_paths.append(all_file_paths)

# Find the maximum number of images
max_images = max([len(paths) for paths in file_paths])

# Iterate over images
for i in range(max_images):
    html_table += "<tr>"
    for j, paths in enumerate(file_paths):
        try:
            image_path = paths[i]
        except IndexError:
            image_path = '/Users/shreya/Documents/GitHub/objaverse-rendering/imgres.html'
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            folder_name = folder_names[j]
            html_table += f"""<td><figure><img src="data:image/jpeg;base64,{base64_image}" alt="{image_path}"><br><br><figcaption><b>{folder_name}</b></figcaption></figure></td>"""
    html_table += "</tr>"

html_table += "</table>"

# Write comparison HTML file
with open("compare_all.html", "w") as html_file:
    html_file.write(html_table)
