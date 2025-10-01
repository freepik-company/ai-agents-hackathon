import os
import requests
from dotenv import load_dotenv

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv()

API_URL = "https://api.freepik.com/v1/videos"

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"),}

# Define parameters and filters for a RECENT search focused on motion graphics
# This example demonstrates: order=recent, category=motion_graphics,
# resolution=4K only, and multiple FPS values.
params = {
    "term": "motion graphics background",  # Required search term
    "page": 1,  # Results page number
    "per_page": 5,  # Results per page (server may cap max value)
    "order": "recent",  # Sort by most recent videos
    "filters[category]": ["motion_graphics"],  # Only motion graphics
    "filters[resolution][720]": False,
    "filters[resolution][1080]": False,
    "filters[resolution][2K]": False,
    "filters[resolution][4K]": True,
    #"filters[fps]": ["30", "60"],  # 30 or 60 fps
    "filters[ai-generated][excluded]": True,
    "filters[ai-generated][only]": False,
}

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

