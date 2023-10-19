import os
from bs4 import BeautifulSoup

# Path to the 'clean' folder
clean_folder = 'clean'

# Path to the parent folder for 'TXT'
parent_folder = os.path.dirname(clean_folder)

# Path to the 'TXT' folder
txt_folder = os.path.join(parent_folder, 'TXT')

# Create 'TXT' folder if it doesn't exist
if not os.path.exists(txt_folder):
    os.makedirs(txt_folder)

# Function to replace problematic characters
def replace_problematic_chars(text):
    problematic_chars = ['\u2028']
    for char in problematic_chars:
        text = text.replace(char, '')
    return text

# Function to convert HTML files to TXT
def convert_html_to_txt(html_path, txt_path):
    with open(html_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        text = replace_problematic_chars(text)
    
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

# Create a log file for conversion output
log_path = os.path.join(txt_folder, 'conversion_log.txt')
log_file = open(log_path, 'w', encoding='utf-8')

# Traverse through the 'clean' folder and its subdirectories
for root, _, files in os.walk(clean_folder):
    for file in files:
        if file.endswith('.html'):
            html_path = os.path.join(root, file)
            relative_path = os.path.relpath(html_path, clean_folder)
            txt_path = os.path.join(txt_folder, relative_path[:-5] + '.txt')
            os.makedirs(os.path.dirname(txt_path), exist_ok=True)
            
            log_line = f"Converting: {relative_path}\n"
            log_file.write(log_line)
            convert_html_to_txt(html_path, txt_path)

log_file.close()
print("Conversion completed. TXT files saved in the 'TXT' folder.")
