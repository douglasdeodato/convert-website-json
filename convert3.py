import os
import json

# Create directory INSIDE_OUT_JOURNAL_ARCHIVE + inside-out-archive-past-editions.html with all links

# Create directory
directory_name = "INSIDE_OUT_JOURNAL_ARCHIVE"
os.makedirs(directory_name, exist_ok=True)

# Read data from JSON file
json_file = "data2.json"

with open(json_file) as f:
    data = json.load(f)

# Generate HTML page with links
html_content = """
<html>
<head>
    <title>Inside Out Journal Archive - Past Editions</title>
</head>
<body>
    <h1>Inside Out Journal Archive</h1>
    <h2>Past Editions</h2>
"""

for item in data["links"]:
    if isinstance(item, dict):
        link_text = item.get("link_text", "Link Text Not Found")
        url_converted = item.get("url_converted")
        
        if url_converted is not None:
            html_content += f'<a href="{url_converted}">{link_text}</a><br>\n'

html_content += """
</body>
</html>
"""

# Save HTML page
html_file = os.path.join(directory_name, "inside-out-archive-past-editions.html")

with open(html_file, "w") as f:
    f.write(html_content)

print(f"HTML page '{html_file}' has been created with the links from '{json_file}'.")
