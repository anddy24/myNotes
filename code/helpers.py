import xml.etree.ElementTree as ET  #pentru import fisiere de limba
import json
import os

def load_language(language_code):
    path = f"language/{language_code}.xml"
    tree = ET.parse(path)
    root = tree.getroot()
    
    strings = {}
    for string in root:
        strings[string.tag] = string.text
    
    return strings

def get_selected_language():
    try:
        with open("settings/settings.json", "r") as f:
            settings = json.load(f)
            return settings.get("language", "english")
    except:
        return "english"