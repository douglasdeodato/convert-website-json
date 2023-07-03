import os
from bs4 import BeautifulSoup

# Function to extract text after href and create a new HTML file
def extract_text_and_create_file(file_path, output_folder):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a')

    for link in links:
        href = link.get('href')
        if href:
            text = href.split('/')[-1]
            new_folder_name = f"{text}"
            new_folder_path = os.path.join(output_folder, new_folder_name)
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)

            new_file_name = f"{text}.html"
            new_file_path = os.path.join(new_folder_path, new_file_name)
            with open(new_file_path, 'w', encoding='utf-8') as new_file:
                new_file.write(f"<html><body>{text}</body></html>")
            print(f"New HTML file created: {new_file_path}")

# Define the input and output folder paths
input_folder = "all_pages"
output_folder = "output"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get the HTML file names from the input folder
html_files = os.listdir(input_folder)

# Iterate over each HTML file
for file_name in html_files:
    file_path = os.path.join(input_folder, file_name)
    if os.path.isfile(file_path):
        print(f"Processing HTML file: {file_path}")
        extract_text_and_create_file(file_path, output_folder)
    else:
        print(f"Ignoring non-file entry: {file_path}")
