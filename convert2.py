import requests
import json
from bs4 import BeautifulSoup
import sys

# Load the data from the data.json file
with open('data.json', 'r') as file:
    data = json.load(file)

# Load the stop condition from the config.json file
with open('config.json', 'r') as file:
    config_data = json.load(file)
stop_condition = config_data['stop_condition']

# Create a list to store all the extracted links
extracted_links = []

# Iterate over the paragraphs in the data
checked_count = 0  # Variable to count the checked links
stop_check = False  # Flag to control the link check

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
                print("\nChecking link:", href)
                print("Text:", text)  # Print the text value
                print(f"{checked_count} link checked\n")  # Print the count message
                sys.stdout.flush()  # Flush the output buffer to show the message immediately

                # Check if the text value matches the stop condition
                if text == stop_condition:
                    stop_check = True
                    break

                # Append the "text" and "url converted" fields to the extracted_links list
                extracted_links.append({
                    "link number checked": checked_count,
                    "text": text,
                    "url converted": href
                })

    else:
        print("\nNo links found.")
        print("Text:", text)  # Print the text value
        sys.stdout.flush()  # Flush the output buffer to show the message immediately

    # Break the loop if the stop condition is met
    if stop_check:
        break

# Create a dictionary to store the extracted links
extracted_data = {
    'stop_condition': stop_condition,
    'links': [None] + extracted_links  # Insert null as the first element
}

# Save the extracted data to a JSON file with formatting
with open('data2.json', 'w') as outfile:
    json.dump(extracted_data, outfile, indent=4)

print("\nData saved to data2.json successfully!")
