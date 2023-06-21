import requests
import json
from bs4 import BeautifulSoup

# Load the URL from the JSON file
with open('config.json', 'r') as file:
    json_data = json.load(file)

# Get the URL from the loaded JSON
url = json_data['site_url']

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
    data['paragraphs'] = [p.get_text() for p in soup.find_all('p')]

    # Extract the h1 and h4 headings from the website
    data['headings'] = {
        'h1': [h1.get_text() for h1 in soup.find_all('h1')],
        'h4': [h4.get_text() for h4 in soup.find_all('h4')]
    }

    # Save the data to a JSON file with formatting
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

    print("Data saved to data.json successfully!")
else:
    print("An error occurred while making the HTTP request. Status code:", response.status_code)
