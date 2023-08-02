import os
import shutil
from bs4 import BeautifulSoup

def delete_elements(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    for table_elem in soup.find_all('table'):
        table_elem.extract()

    for div_elem in soup.find_all('div', class_='als-viewport'):
        div_elem.extract()

    for script_elem in soup.find_all('script', type='text/javascript'):
        script_elem.extract()

    for img_elem in soup.find_all('img', alt='', border='0', height='115', width='450'):
        img_elem.extract()

    return str(soup)

def process_files(src_folder, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for root, _, files in os.walk(src_folder):
        for filename in files:
            if filename.endswith(".html"):
                src_file = os.path.join(root, filename)
                dest_file = os.path.join(dest_folder, os.path.relpath(src_file, src_folder))

                with open(src_file, 'r', encoding='utf-8') as file:
                    html_content = file.read()

                cleaned_html = delete_elements(html_content)

                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                with open(dest_file, 'w', encoding='utf-8') as file:
                    file.write(cleaned_html)

if __name__ == "__main__":
    src_folder = "issue-all-links-printed"
    dest_folder = "clean"

    process_files(src_folder, dest_folder)
