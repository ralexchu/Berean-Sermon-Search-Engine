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
    download_transcripts()  # Currently a placeholder.
    
    # Print the project root (one level above this file).
    print(Path(__file__).resolve().parents[1])
    
def download_video_details():
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
    # API URL for the transcripts folder.
    api_url = "https://api.github.com/repos/lawwu/berean_transcripts/contents/data/transcripts/"
    
    # GitHub authentication using environment variables.
    auth = (os.getenv('GITHUB_USERNAME'), os.getenv('GITHUB_TOKEN'))
    
    # Fetch the contents of the transcripts folder from GitHub.
    response = requests.get(api_url, auth=auth)
    response.raise_for_status()
    data = response.json()
    
    # Get the local folder path and ensure it exists.
    local_folder = get_transcripts_path()
    local_folder.mkdir(parents=True, exist_ok=True)
    
    # Create a set of existing file names in the local folder.
    existing_files = {file.name for file in local_folder.iterdir() if file.is_file()}
    
    # Iterate through each file in the GitHub folder.
    for item in data:
        if item.get('type') == 'file':
            filename = item.get("name")
            if filename in existing_files:
                print(f"Skipping {filename} (already downloaded).")
            else:
                download_url = item.get("download_url")
                if download_url:
                    file_response = requests.get(download_url, auth=auth)
                    file_response.raise_for_status()
                    file_path = local_folder / filename
                    # Save the transcript as a text file.
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(file_response.text)
                    print(f"Downloaded transcript: {file_path}")
                    # Add the filename to the set to track downloaded files.
                    existing_files.add(filename)
                else:
                    print(f"Download URL missing for file: {filename}")

if __name__ == '__main__':
    main()
