# app/utils.py
import json
import logging
import os
import re
import bleach
from config import get_config

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def load_json_data():
    """Load data from JSON (users, stories)."""
    cfg = get_config()
    try:
        if not os.path.exists(cfg.JSON_DATA_FILE):
            # If file doesn't exist, create a basic template
            with open(cfg.JSON_DATA_FILE, 'w') as f:
                json.dump({"users": [], "stories": []}, f)
        with open(cfg.JSON_DATA_FILE, 'r') as f:
            data = json.load(f)
        return data
    except (IOError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load JSON data: {e}")
        return {"users": [], "stories": []}

def save_json_data(data):
    """Save data to JSON file."""
    cfg = get_config()
    try:
        with open(cfg.JSON_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        logging.error(f"Failed to save JSON data: {e}")

def sanitize_input(user_input):
    """
    Sanitize the user input by:
    1. Stripping HTML tags using bleach.clean.
    2. Removing special characters that could lead to injection attacks.
    """
    # Remove any HTML or script content
    cleaned = bleach.clean(user_input, strip=True)
    # You can further strip out other special characters if desired:
    # Example: removing semicolons, angle brackets, quotes, etc.
    cleaned = re.sub(r'[<>\'";]', '', cleaned)
    return cleaned

def check_disallowed_words(text):
    """
    Check if text contains any disallowed word.
    Case-insensitive and partial matches are flagged.
    Returns a list of found disallowed words or an empty list if none found.
    """
    cfg = get_config()
    disallowed_found = []
    if not os.path.exists(cfg.DISALLOWED_WORDS_FILE):
        logging.warning("Disallowed words file not found.")
        return disallowed_found

    with open(cfg.DISALLOWED_WORDS_FILE, 'r') as f:
        disallowed_words = [w.strip().lower() for w in f.readlines() if w.strip()]

    text_lower = text.lower()
    for dw in disallowed_words:
        # Check partial matches using substring check
        if dw in text_lower:
            disallowed_found.append(dw)

    return disallowed_found

def log_event(message, level='INFO'):
    """
    Log events with specified log level.
    Levels can be INFO, WARNING, ERROR, DEBUG, etc.
    """
    if level == 'INFO':
        logging.info(message)
    elif level == 'WARNING':
        logging.warning(message)
    elif level == 'ERROR':
        logging.error(message)
    elif level == 'DEBUG':
        logging.debug(message)
    else:
        logging.info(message)