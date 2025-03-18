# utils/helpers.py
import os
import json
from datetime import datetime

def load_template(template_name):
    """Load a template file"""
    template_path = os.path.join("templates", template_name)
    if os.path.exists(template_path):
        with open(template_path, "r") as file:
            return file.read()
    return ""

def generate_artifact_id(prefix, project_id):
    """Generate a unique ID for an artifact"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{prefix}_{project_id}_{timestamp}"

def save_artifact_to_file(artifact_id, content, directory="artifacts"):
    """Save an artifact to a file for backup purposes"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    filename = os.path.join(directory, f"{artifact_id}.txt")
    with open(filename, "w") as file:
        file.write(content)
    return filename

def extract_keywords(text):
    """Extract keywords from text for better retrieval"""
    # Simplified implementation - in a real system you might use NLP
    words = text.lower().split()
    stopwords = ["the", "a", "an", "in", "on", "at", "to", "for", "with", "by"]
    keywords = [word for word in words if word not in stopwords and len(word) > 3]
    return list(set(keywords[:20]))  # Return up to 20 unique keywords