import os
from bs4 import BeautifulSoup
import re


# creates the main file linking all the links converted.

def clean_link_text(link_text):
    # Remove invalid characters from the link text for the file name
    cleaned_text = re.sub(r'[\\/:"*?<>|]', '', link_text.strip())
    return cleaned_text.replace(' ', '_').replace(':', '_')

def replace_links(source_file, batch_folder):
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
            # Check if the corresponding folder exists in "issue-all-links-printed"
            folder_name = os.path.splitext(os.path.basename(source_file))[0]
            matched_folder = os.path.join("issue-all-links-printed", folder_name)
            if os.path.exists(matched_folder):
                # Get the name of the corresponding HTML file from the matched folder
                html_file_name = f"{clean_link_text(link_text)}.html"
                html_file_path = os.path.join(matched_folder, html_file_name)
                
                if os.path.exists(html_file_path):
                    # Replace the href link in the original HTML file with the correct one
                    link_tag["href"] = f"{html_file_name}"

        # Add <br> after each link
        link_tag.insert_after(soup.new_tag("br"))

    # Save the updated content to the matched page file
    matched_file_name = f"{folder_name}.html"
    matched_file_path = os.path.join(batch_folder, matched_file_name)
    with open(matched_file_path, "wb") as matched_file:
        matched_file.write(soup.prettify().encode('utf-8'))

    print(f"Page matched and saved to '{matched_file_name}'.", flush=True)

if __name__ == "__main__":
    # Enter the "pages-links" directory
    directory = "INSIDE_OUT_JOURNAL_ARCHIVE/pages-links"

    # Process each HTML file in the "pages-links" directory
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            source_file = os.path.join(directory, filename)
            # Get the name of the file (excluding the extension) to create a folder with that name
            file_name = os.path.splitext(filename)[0]
            batch_folder = os.path.join("issue-all-links-printed", file_name)
            os.makedirs(batch_folder, exist_ok=True)
            replace_links(source_file, batch_folder)
