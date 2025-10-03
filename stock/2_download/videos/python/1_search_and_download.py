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
    "filters[license][free]":1,  
}

# Make the API request
response = requests.get(API_URL, headers=headers, params=params)

if response.status_code == 200:
    # DOWNLOAD API CODE HERE --------------------------------------------------------
    RESOURCE_ID = response.json()["data"][0]["id"]
    API_DOWNLOAD_URL = f"https://api.freepik.com/v1/videos/{RESOURCE_ID}/download"

    params = {
        "image_size": "small", # Possible values: small, medium, large, original
        } 
    response = requests.get(API_DOWNLOAD_URL, headers=headers)#, params=params)

    if response.status_code == 200:
        url_video = response.json()["data"]["url"]
        if url_video:
            # Save the image in the same directory as this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_name = os.path.join(current_dir, f"{RESOURCE_ID}.mp4")
            video_response = requests.get(url_video)
            if video_response.status_code == 200:
                with open(file_name, "wb") as f:
                    f.write(video_response.content)
                print(f"Video successfully downloaded as {file_name}")
            else:
                print(f"Could not download the video. Status code: {video_response.status_code}")
        else:
            print("Video URL not found in the response.")
    else:
        print(f"Error while downloading the video. Status code: {response.status_code}, message: {response.json()['message']}")
else:
    print(f"Error while searching the video. Status code: {response.status_code}, message: {response.json()['message']}")
