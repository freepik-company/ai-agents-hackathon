import os
import requests
from dotenv import load_dotenv

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv() 

API_URL = "https://api.freepik.com/v1/videos"

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY")}

# Define the parameters and filters for the API request
params = {
    "term": "beautiful landscape", # Search term
    "page": 1, # Results page number
    "order": "relevance", # Order by relevance, other options: recent
    #"filters[aspect_ratio]": ["243", "61"], # Filter by aspect ratio, possible values: 61, 243, 556, 969, 256:135
    "filters[category]": ["footage"], # Filter by category, possible values: footage, motion_graphics
    #"filters[orientation]": ["horizontal", "panoramic"], # Filter by orientation, possible values: horizontal, vertical, square, panoramic
    "filters[resolution][720]": 1,
    "filters[resolution][1080]": 1,
    "filters[resolution][2K]": 0,
    "filters[resolution][4K]": 0,
    #"filters[fps]": [30, 60], # Filter by fps, possible values: 24, 25, 30, 60, gt60
    #"filters[topic]": ["nature", "background", "travel"], # Filter by topic, possible values: npeople, nature, business, background, food, travel, sports, events
    "filters[ai-generated][excluded]": 1,
    "filters[ai-generated][only]": 0,    
}

# Make the API request
response = requests.get(API_URL, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Iterate over the response data
    for r in response.json()["data"]:
        for k, v in r.items():
            print(f"{k}: {v}")
        print("-"*30)
# If the request was not successful, print the error
else:
    print(response.status_code, response.text)

