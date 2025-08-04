# File Management Templates
# Week 1 - Road to AI Agent Engineer

import os
import json
from typing import Dict, Any, List

def create_directory(path: str):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)

def save_json(data: Dict[str, Any], filename: str):
    """Save data to JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

def load_json(filename: str) -> Dict[str, Any]:
    """Load data from JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def append_to_json(data: Dict[str, Any], filename: str):
    """Append data to existing JSON file."""
    existing_data = load_json(filename)
    if isinstance(existing_data, list):
        existing_data.append(data)
    else:
        existing_data = [existing_data, data]
    
    save_json(existing_data, filename)

def list_files(directory: str, extension: str = None) -> List[str]:
    """List files in directory."""
    files = []
    for file in os.listdir(directory):
        if extension and not file.endswith(extension):
            continue
        files.append(file)
    return files 