import os
import requests
from dotenv import load_dotenv

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv() 

API_URL = "https://api.freepik.com/v1/icons"

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY")}

# Define the parameters and filters for the API request
params = {
    "term": "a mechanic taller", # Search term
    "slug": "repair", # Search using also tags
    "page": 1, # Results page number
    "per_page": 1, # Number of results per page
    "order": "relevance", # Order by relevance, other options: recent
    "thumbnail_size": 256, # Thumbnail size -> default: 128
    "filters[color]": ["green", "orange",], # Filter by color, possible values: gradient, solid-black, multicolor, azure, black, blue, chartreuse, cyan, gray, green, orange, red, rose, spring-green, violet, white, yellow 
    "filters[shape]": ["outline", "fill"], # Filter by shape, possible values: outline, fill, lineal-color, hand-drawn
}

# Make the API request
response = requests.get(API_URL, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    RESOURCE_ID = response.json()["data"][0]["id"]
    API_DOWNLOAD_URL = f"https://api.freepik.com/v1/icons/{RESOURCE_ID}/download"

    params = {
        "format": "png", # Possible values: svg, png, gif, mp4, aep, json, psd, eps
        "png_size": 64, # Possible values: 512, 256, 128, 64, 32, 24, 16 (only for png format)
        }
    response = requests.get(API_DOWNLOAD_URL, headers=headers, params=params)

    if response.status_code == 200:
        url_icon = response.json()["data"]["url"]
        if url_icon:
            # Save the image in the same directory as this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_name = os.path.join(current_dir, f"{RESOURCE_ID}.png")
            icon_response = requests.get(url_icon)
            if icon_response.status_code == 200:
                with open(file_name, "wb") as f:
                    f.write(icon_response.content)
                print(f"Icon successfully downloaded as {file_name}")
            else:
                print(f"Could not download the icon. Status code: {icon_response.status_code}")
        else:
            print("Icon URL not found in the response.")
    else:
        print(f"Error while downloading the icon. Status code: {response.status_code}, message: {response.json()['message']}")
else:
    print(f"Error while searching the icon. Status code: {response.status_code}, message: {response.json()['message']}")

