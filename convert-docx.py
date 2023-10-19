import os
from bs4 import BeautifulSoup
from docx import Document

# Path to the 'clean' folder
clean_folder = 'clean'

# Path to the parent folder for 'DOCX'
parent_folder = os.path.dirname(clean_folder)

# Path to the 'DOCX' folder
docx_folder = os.path.join(parent_folder, 'DOCX')

# Create 'DOCX' folder if it doesn't exist
if not os.path.exists(docx_folder):
    os.makedirs(docx_folder)

# Function to replace problematic characters
def replace_problematic_chars(text):
    problematic_chars = ['\u2028']
    for char in problematic_chars:
        text = text.replace(char, '')
    return text

# Function to convert HTML files to DOCX files
def convert_html_to_docx(html_path, docx_path):
    doc = Document()
    with open(html_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        text = replace_problematic_chars(text)
        
        # Add text to the Word document
        doc.add_paragraph(text)
    
    doc.save(docx_path)

# Create a log file for conversion output
log_path = os.path.join(docx_folder, 'conversion_log.txt')
log_file = open(log_path, 'w', encoding='utf-8')

# Traverse through the 'clean' folder and its subdirectories
for root, _, files in os.walk(clean_folder):
    for file in files:
        if file.endswith('.html'):
            html_path = os.path.join(root, file)
            relative_path = os.path.relpath(html_path, clean_folder)
            docx_path = os.path.join(docx_folder, relative_path[:-5] + '.docx')
            os.makedirs(os.path.dirname(docx_path), exist_ok=True)
            
            log_line = f"Converting: {relative_path}\n"
            log_file.write(log_line)
            convert_html_to_docx(html_path, docx_path)

log_file.close()
print("Conversion completed. Word files saved in the 'DOCX' folder.")
