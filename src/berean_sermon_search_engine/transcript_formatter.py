import json
from pathlib import Path
from utils import get_video_details_path, get_transcripts_path, get_processed_path

def load_video_details(json_path: Path) -> dict:
    """
    Loads the video details JSON file.

    Args:
        json_path (Path): Path to the JSON file.

    Returns:
        dict: The loaded video details as a dictionary.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def save_video_details(data: dict, output_path: Path):
    """
    Saves the updated video details to a JSON file.

    Args:
        data (dict): The updated video details.
        output_path (Path): Path to the output JSON file.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Updated video details saved to {output_path}")

def add_transcripts_to_details(video_details: dict, transcripts_folder: Path) -> dict:
    """
    Iterates over transcript files in the transcripts folder and adds the
    transcript content to the corresponding video detail entry if it hasn't 
    already been added.

    Matching is done by comparing the filename (without the .txt extension)
    to the video id keys in the video_details dictionary.

    If a transcript is already present (i.e. the "transcript" key exists), that 
    file is skipped to avoid duplicate entries.

    Args:
        video_details (dict): Dictionary of video details.
        transcripts_folder (Path): Path to the folder containing transcript text files.

    Returns:
        dict: The updated video details with transcripts added.
    """
    count = 0
    for transcript_file in transcripts_folder.glob("*.txt"):
        video_id = transcript_file.stem  # Filename without extension
        transcript_text = transcript_file.read_text(encoding='utf-8').strip()
        if video_id in video_details:
            if "transcript" in video_details[video_id]:
                print(f"Transcript already added for video id: {video_id}. Skipping.")
            else:
                video_details[video_id]["transcript"] = transcript_text
                print(f"Added transcript for video id: {video_id}")
            count+=1
        else:
            print(f"No matching video details found for transcript file: {transcript_file.name}")
    print(f'COUNT: {count}')
    return video_details

def main():
    """
    Main function to load video details, update them with transcript texts,
    and write out the updated JSON to the processed folder.
    """
    # Get the raw video details JSON from the raw folder.
    raw_video_details_path = get_video_details_path() / 'video_details_cache.json'
    transcripts_folder = get_transcripts_path()
    
    # Load the existing video details JSON data.
    video_details = load_video_details(raw_video_details_path)
    
    # Update the video details with transcript text (only add new ones).
    updated_details = add_transcripts_to_details(video_details, transcripts_folder)
    
    # Save the updated JSON to the processed folder.
    output_path = get_processed_path() / 'video_details_cache_with_transcripts.json'
    save_video_details(updated_details, output_path)

if __name__ == '__main__':
    main()
