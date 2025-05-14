import xml.etree.ElementTree as ET  #pentru import fisiere de limba

def load_language(language_code):
    path = f"language/{language_code}.xml"
    tree = ET.parse(path)
    root = tree.getroot()
    
    strings = {}
    for string in root:
        strings[string.tag] = string.text
    
    return strings



import json

def load_user_language():
    try:
        with open("../settings/settings.json") as f:
            settings = json.load(f)
            return settings.get("language", "english")
    except FileNotFoundError:
        return "english"