import requests
import json
from bs4 import BeautifulSoup

# Load the URL and base URL from the JSON file
with open('config.json', 'r') as file:
    json_data = json.load(file)

url = json_data['site_url']
base_url = json_data['base_url']

# Make an HTTP request to retrieve the HTML content of the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Create an empty dictionary to store the data
    data = {}

    # Extract the website title
    data['title'] = soup.title.string

    # Extract the paragraphs from the website
    paragraphs = soup.find_all('p')
    data['paragraphs'] = []

    # Extract the <a> tags within the paragraphs and include the href links
    for paragraph in paragraphs:
        paragraph_data = {
            'text': paragraph.get_text(),
            'links': []
        }

        links = paragraph.find_all('a')
        for link in links:
            href = link.get('href')
            # Insert the base URL from the JSON file before the href value
            full_href = base_url + href if href else ""
            paragraph_data['links'].append({
                'text': link.get_text(),
                'href': full_href
            })

        data['paragraphs'].append(paragraph_data)

    # Save the data to a JSON file with formatting
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

    print("Data saved to data.json successfully!")
else:
    print("An error occurred while making the HTTP request. Status code:", response.status_code)
