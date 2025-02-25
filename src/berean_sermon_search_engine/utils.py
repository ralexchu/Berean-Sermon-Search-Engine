import logging
from pathlib import Path

def get_project_root():
    return Path(__file__).resolve().parents[2]

def get_data_path():
    return get_project_root() / 'data'

def get_raw_path():
    return get_data_path() / 'raw'

def get_processed_path():
    return get_data_path() / 'processed'

def get_transcripts_path():
    # Transcripts are located in data/raw/transcripts
    return get_raw_path() / 'transcripts'

def get_video_details_path():
    # Video details are located in data/raw/video_details
    return get_raw_path() / 'video_details'

def setup_logging(log_level=logging.INFO):
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logging.info("Logging is set up.")
