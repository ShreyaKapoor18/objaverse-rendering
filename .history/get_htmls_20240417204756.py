import os
import base64

# Function to generate HTML content for a directory
def generate_html(directory_path):
    # Initialize HTML content
    html_content = f"""<!DOCTYPE html>
        <html>
        <head>
            <title>Images Gallery</title>
        </head>
        <body>
            <h1>Images Gallery</h1>
        """

    # Traverse through the directory and its subdirectories
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                full_image_path = os.path.join(root, file)
                image_name = os.path.splitext(file)[0]
                with open(full_image_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode("utf-8")
                    html_content += f"""<h2>{image_name}</h2><figure><img src="data:image/jpeg;base64,{base64_image}" alt="{full_image_path}"><br><br><figcaption>{full_image_path}</figcaption></figure>"""

    # Close the HTML content
    html_content += "</body></html>"
    return html_content

# Define the directory path
import glob
directory_path = '/Users/shreya/Documents/GitHub/objaverse-rendering/jsons'
from os.path import join
for directory in glob.glob(join(directory_path, '*')):

    # Generate HTML content
    html_content = generate_html(directory_path)
    half_name = directory_path.split('/')[-1]
    print(half_name)
    # Write HTML file
    with open(f"{half_name}.html", "w") as html_file:
        html_file.write(html_content)
