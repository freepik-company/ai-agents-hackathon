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
    "per_page": 5, # Number of results per page
    "order": "relevance", # Order by relevance, other options: recent
    "thumbnail_size": 256, # Thumbnail size -> default: 128
    "filters[color]": ["green", "orange",], # Filter by color, possible values: gradient, solid-black, multicolor, azure, black, blue, chartreuse, cyan, gray, green, orange, red, rose, spring-green, violet, white, yellow 
    "filters[shape]": ["outline", "fill"], # Filter by shape, possible values: outline, fill, lineal-color, hand-drawn
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

