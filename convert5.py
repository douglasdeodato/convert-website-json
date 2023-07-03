import os


#create inside all pages folder / archive and all the folders with the links names 

# Function to create folders for each HTML file name
def create_folders(html_files):
    # Create the "archive" folder inside "INSIDE_OUT_JOURNAL_ARCHIVE\all_pages" directory
    archive_folder = os.path.join("all_pages", "archive")
    os.makedirs(archive_folder, exist_ok=True)

    # Create folders for each HTML file name
    for file_name in html_files:
        folder_name = os.path.splitext(file_name)[0]
        folder_path = os.path.join(archive_folder, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Folder created: {folder_path}", flush=True)

# Get the HTML file names from the "INSIDE_OUT_JOURNAL_ARCHIVE\all_pages" directory
html_files = os.listdir(os.path.join( "all_pages"))

# Create folders for each HTML file name
create_folders(html_files)
