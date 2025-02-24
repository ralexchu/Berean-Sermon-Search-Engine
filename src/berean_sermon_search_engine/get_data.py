import os
import requests
import json
from dotenv import load_dotenv
from pathlib import Path
from utils import get_transcripts_path, get_video_details_path

def main():
    # Load environment variables from the .env file.
    load_dotenv()
    
    download_video_details()
    download_transcripts()  
    
def download_video_details():
    """
    Downloads the video_details_cache.json file from the GitHub repository
    and saves it to the local path specified by get_video_details_path().
    
    It performs the following steps:
        1. Fetches file metadata from the GitHub API.
        2. Extracts the download URL from the metadata.
        3. Downloads the raw JSON content.
        4. Saves the content as a text file to the designated local directory.
    """
    # Construct the API URL for file metadata.
    api_url = "https://api.github.com/repos/lawwu/berean_transcripts/contents/data/video_details_cache.json"
    
    # Use environment variables for GitHub authentication.
    auth = (os.getenv('GITHUB_USERNAME'), os.getenv('GITHUB_TOKEN'))
    response = requests.get(api_url, auth=auth)
    response.raise_for_status()
    
    # Get the metadata, which includes the download URL.
    file_metadata = response.json()
    download_url = file_metadata.get("download_url")
    if not download_url:
        raise Exception("Download URL not found in the file metadata.")
    
    # Download the raw JSON file content.
    file_response = requests.get(download_url, auth=auth)
    file_response.raise_for_status()
    
    # Define the local file path.
    file_path = get_video_details_path() / 'video_details_cache.json'
    
    # Save the file as text.
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(file_response.text)
    
    print(f"Downloaded video details to {file_path}")
    
def download_transcripts():
    """
    Downloads transcript text files from the GitHub repository folder:
    data/transcripts/
    
    This function uses the Git Trees API with recursive=1 to overcome the 
    1000-item limitation of the standard contents API. It performs the following:
        1. Retrieves the complete repository tree.
        2. Filters for files located in data/transcripts/.
        3. Checks the local transcripts directory for already downloaded files.
        4. Downloads and saves only new transcript files, preserving their names.
    """
    owner = "lawwu"
    repo = "berean_transcripts"
    branch = "main"  # Adjust if your default branch is different
    
    # Construct the Git Trees API URL with recursive=1.
    tree_api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    
    auth = (os.getenv('GITHUB_USERNAME'), os.getenv('GITHUB_TOKEN'))
    response = requests.get(tree_api_url, auth=auth)
    response.raise_for_status()
    tree_data = response.json()
    
    # Filter for files in the transcripts folder.
    transcript_files = [
        item for item in tree_data.get("tree", [])
        if item["type"] == "blob" and item["path"].startswith("data/transcripts/")
    ]
    
    # Get the local folder to save transcripts.
    local_folder = get_transcripts_path()
    local_folder.mkdir(parents=True, exist_ok=True)
    
    # Create a set of already downloaded file names.
    existing_files = {file.name for file in local_folder.iterdir() if file.is_file()}
    
    for item in transcript_files:
        filename = item["path"].split("/")[-1]
        if filename in existing_files:
            print(f"Skipping {filename} (already downloaded).")
        else:
            # Construct the raw URL for the file.
            raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{item['path']}"
            file_response = requests.get(raw_url, auth=auth)
            file_response.raise_for_status()
            
            file_path = local_folder / filename
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(file_response.text)
            print(f"Downloaded transcript: {file_path}")
            existing_files.add(filename)

if __name__ == '__main__':
    main()