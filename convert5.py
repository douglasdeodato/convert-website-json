import os
import requests
from bs4 import BeautifulSoup
import re
import string
import time
import sys

# Set the console encoding to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Function to remove non-printable characters from the content
def remove_non_printable(content):
    printable_chars = set(string.printable)
    return ''.join(filter(lambda x: x in printable_chars, content))

# Function to create a page for each link
def create_page(source_file, batch_folder):
    # Define invalid characters for the file name
    invalid_chars = r'\/:*?"<>|'

    # Read the HTML file
    with open(source_file, encoding="utf-8") as f:
        html_content = f.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all <a> tags
    link_tags = soup.find_all("a")

    for link_tag in link_tags:
        link_text = link_tag.get_text()
        url = link_tag.get("href")

        if url is not None:
            # Send a GET request to the URL
            response = requests.get(url)
            if response.status_code == 200:
                # Extract the content inside the div elements with id="id_FA6BOdP", id="id_nVkvGep", id="id_Fe3QN4i", and class="gadgetStyleBody gadgetContentEditableArea"
                linked_html_content = BeautifulSoup(response.text, "html.parser").find_all("div", {"id": ["id_FA6BOdP", "id_nVkvGep", "id_Fe3QN4i"]})
                editable_area_content = BeautifulSoup(response.text, "html.parser").find("div", {"class": "gadgetStyleBody gadgetContentEditableArea"})
                class_content = BeautifulSoup(response.text, "html.parser").find("div", {"class": "WaGadgetLast WaGadgetContent gadgetStyleNone"})

                if linked_html_content and editable_area_content:
                    # Combine both contents
                    combined_content = ""
                    for content in linked_html_content:
                        # Exclude the unwanted divs
                        if 'id_Fe3QN4i' not in str(content) and 'gadgetStyleNone' not in str(content):
                            combined_content += str(content)
                    combined_content += str(editable_area_content)

                    # Remove unusual line terminators from the combined content
                    combined_content = combined_content.replace('\r\n', '\n').replace('\r', '\n')

                    # Remove non-printable characters and control characters from the content
                    combined_content = remove_non_printable(combined_content)

                    # Generate the file name based on the link text
                    # Replace spaces with underscores and remove any invalid characters from the link text for the file name
                    file_name = re.sub('_+', '_', ''.join(c if c not in invalid_chars else '_' for c in link_text.strip().replace(' ', '_')))

                    # Remove any newline characters from the file_name
                    file_name = file_name.replace('\n', '')

                    # Save the combined content to the file in binary mode with UTF-8 encoding
                    file_path = os.path.join(batch_folder, f"{file_name}.html")
                    with open(file_path, "wb") as f:
                        f.write(combined_content.encode('utf-8'))

                    print(f"Page created for '{link_text}' at '{file_path}'.", flush=True)
                elif class_content:
                    # Only class="WaGadgetLast WaGadgetContent gadgetStyleNone" content is found
                    # Remove unusual line terminators from the class content
                    class_content = str(class_content).replace('\r\n', '\n').replace('\r', '\n')

                    # Remove non-printable characters and control characters from the content
                    class_content = remove_non_printable(class_content)

                    # Generate the file name based on the link text
                    # Replace spaces with underscores and remove any invalid characters from the link text for the file name
                    file_name = re.sub('_+', '_', ''.join(c if c not in invalid_chars else '_' for c in link_text.strip().replace(' ', '_')))
                    file_name = file_name.replace('\n', '')

                    # Save the content to the file in binary mode with UTF-8 encoding
                    file_path = os.path.join(batch_folder, f"{file_name}.html")
                    with open(file_path, "wb") as f:
                        f.write(class_content.encode('utf-8'))
                    print(f"Page created for '{link_text}' at '{file_path}' (using class content).", flush=True)
                else:
                    print(f"No div with id='id_FA6BOdP', id='id_nVkvGep', id='id_Fe3QN4i', or class='gadgetStyleBody gadgetContentEditableArea' found in the linked content for '{link_text}'.", flush=True)
            else:
                print(f"Failed to retrieve content for '{link_text}'. Status code: {response.status_code}", flush=True)

if __name__ == "__main__":
    # Enter the "pages-links" directory
    directory = "INSIDE_OUT_JOURNAL_ARCHIVE/pages-links"

    # Create the "issue-all-links-printed" directory if it doesn't exist
    output_directory = "issue-all-links-printed"
    os.makedirs(output_directory, exist_ok=True)

    # Get the list of already processed folders
    processed_folders = set(os.listdir(output_directory))

    # Process each HTML file in the "pages-links" directory
    count_folders = 0  # Count of folders created
    last_batch = False  # Flag to check if it's the last batch
    batch_size = 10  # Number of folders to create in a batch

    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            source_file = os.path.join(directory, filename)
            # Get the name of the file (excluding the extension) to create a folder with that name
            file_name = os.path.splitext(filename)[0]
            batch_folder = os.path.join("issue-all-links-printed", file_name)
            
            # Skip already processed folders
            if file_name in processed_folders:
                print(f"Skipping folder '{file_name}' as it's already processed.")
                continue
            
            os.makedirs(batch_folder, exist_ok=True)
            create_page(source_file, batch_folder)

            count_folders += 1
            if count_folders % batch_size == 0:
                print(f"Waiting for 5 seconds before proceeding to the next batch...", flush=True)
                time.sleep(5)  # 5-second delay before continuing to the next batch

            if count_folders == len(os.listdir(directory)):
                last_batch = True

    if not last_batch:
        remaining_folders = count_folders % batch_size
        if remaining_folders > 0:
            print(f"Waiting for 5 seconds before proceeding to the next batch...", flush=True)
            time.sleep(5)  # 5-second delay before continuing to the next batch
