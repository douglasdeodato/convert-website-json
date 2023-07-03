import os
import requests
from bs4 import BeautifulSoup

# create a folder < all_pages > with all the links with the text inside sample:
# Issue_01__Summer_1990.html + editorial and all links from that page 

# Function to create a page for each link
def create_page(url, link_text):
    # Send a GET request to the URL
    response = requests.get(url)
    if response.status_code == 200:
        # Extract the HTML content
        html_content = response.text

        # Create a subfolder "all_pages" if it doesn't exist
        subfolder = "INSIDE_OUT_JOURNAL_ARCHIVE/pages-links"
        os.makedirs(subfolder, exist_ok=True)

        # Generate the file name based on the link text
        # Replace spaces with underscores and remove any invalid characters from the link text for the file name
        invalid_chars = r'\/:*?"<>|'
        file_name = ''.join(c if c not in invalid_chars else '_' for c in link_text.strip().replace(' ', '_'))

        # Create the file path
        file_path = os.path.join(subfolder, f"{file_name}.html")

        # Parse the HTML content
        soup = BeautifulSoup(html_content, "html.parser")

        # Find the <div> elements with the specified ids
        div_elements = soup.find_all("div", {"id": ["id_uQ9f1KA", "id_JtQv6yn"]})

        links = []
        for div_element in div_elements:
            # Find all <a> tags inside the <div> element
            link_tags = div_element.find_all("a")

            # Extract href and text for each <a> tag
            for link_tag in link_tags:
                href = "https://iahip.org" + link_tag.get("href")
                text = link_tag.get_text()
                links.append({"href": href, "text": text})

        if links:
            # Save the links to the file with UTF-8 encoding
            with open(file_path, "w", encoding="utf-8") as f:
                for link in links:
                    f.write(f"<a href='{link['href']}'>{link['text']}</a>\n")

            print(f"Page created for '{link_text}' at '{file_path}'.", flush=True)
        else:
            print(f"No matching divs found for '{link_text}'.", flush=True)
    else:
        print(f"Failed to retrieve content for '{link_text}'. Status code: {response.status_code}", flush=True)

# Read the HTML file
html_file = "INSIDE_OUT_JOURNAL_ARCHIVE/inside-out-archive-past-editions.html"

with open(html_file, encoding="latin-1") as f:
    html_content = f.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Find all <a> tags
link_tags = soup.find_all("a")

# Process each <a> tag
for link_tag in link_tags:
    link_text = link_tag.get_text()
    url = link_tag.get("href")

    if url is not None:
        create_page(url, link_text)
