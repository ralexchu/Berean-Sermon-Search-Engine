import logging
from pathlib import Path

def get_project_root():
    return Path(__file__).resolve().parents[2]

def get_data_path():
    return get_project_root() / 'data'
 
def get_transcripts_path():
    return get_data_path() / 'transcripts'
    
def get_video_details_path():
    return get_data_path() / 'video_details'
    
    

def setup_logging(log_level=logging.INFO):
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logging.info("Logging is set up.")