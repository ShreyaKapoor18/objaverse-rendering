import os
import base64

# Function to generate HTML content for a directory
def generate_html(directory_path):
    # Initialize HTML content
    html_content = f"""<!DOCTYPE html>
        <html>
        <head>
            <title>Images Gallery</title>
            <style>
                .folder-section {{
                    display: flex;
                    flex-wrap: wrap;
                    margin-bottom: 20px;
                }}
                .folder-section img {{
                    margin: 5px;
                    max-width: 10%;
                }}
            </style>
        </head>
        <body>
            <h1>Images Gallery</h1>
        """

    # Traverse through the directory and its subdirectories
    for root, dirs, files in os.walk(directory_path):
        # Split the root directory to get the folder name
        folder_name = os.path.basename(root)
        # Start a new section for each folder
        html_content += f'<div class="folder-section" id="{folder_name}">'
        
        # Counter to keep track of the number of images
        image_count = 0
        
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                full_image_path = os.path.join(root, file)
                image_name = os.path.splitext(file)[0]
                with open(full_image_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode("utf-8")
                    html_content += f"""<img src="data:image/jpeg;base64,{base64_image}" alt="{full_image_path}" title="{image_name}">"""
                
                # Increment image count
                image_count += 1
                
                # Break the loop if 10 images are already added
                if image_count == 10:
                    break

        # Close the section for the current folder
        html_content += "</div>"

    # Close the HTML content
    html_content += "</body></html>"
    return html_content



directory_path = '/Users/shreya/Documents/GitHub/objaverse-rendering/jsons'
import glob
for directory in glob.glob(directory_path, '*'):
    # Generate HTML content
    html_content = generate_html(directory)

    # Write HTML file
    with open(html_content, "w") as html_file:
        html_file.write(html_content)