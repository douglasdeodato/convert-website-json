import requests
import json
from bs4 import BeautifulSoup
import sys

# Load the data from the data.json file
with open('data.json', 'r') as file:
    data = json.load(file)

# Create a list to store all the extracted href links
extracted_links = []

# Iterate over the paragraphs in the data
checked_count = 0  # Variable to count the checked links

for paragraph_data in data['paragraphs']:
    text = paragraph_data['text']
    links = paragraph_data['links']
    if links:
        for link in links:
            href = link['href']
            if href:
                # Make an HTTP request to the linked page
                response = requests.get(href)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # Find all <a> tags on the linked page and extract the href values
                    linked_hrefs = [a.get('href') for a in soup.find_all('a')]
                    # Append the href values to the extracted_links list
                    extracted_links.extend(linked_hrefs)
                checked_count += 1
                print("Checking link:", href)
                print("Text:", text)  # Print the text value
                print(f"{checked_count} link checked")  # Print the count message
                sys.stdout.flush()  # Flush the output buffer to show the message immediately
    else:
        print("No links found.")
        print("Text:", text)  # Print the text value
        sys.stdout.flush()  # Flush the output buffer to show the message immediately

# Create a dictionary to store the extracted links
extracted_data = {
    'links': extracted_links
}

# Save the extracted data to a JSON file with formatting
with open('data2.json', 'w') as outfile:
    json.dump(extracted_data, outfile, indent=4)

print("Data saved to data2.json successfully!")
