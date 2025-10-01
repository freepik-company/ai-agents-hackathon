import os
import requests
from dotenv import load_dotenv

# Load FREEPIK_API_KEY from .env or environment variables
load_dotenv()

API_URL = "https://api.freepik.com/v1/resources"

headers = {
    "x-freepik-api-key": os.getenv("FREEPIK_API_KEY"),
    "Accept-Language": "es-ES", # Demonstration with Spanish as default language
}

# Example: search for recent PSDs of "atardecer playa" in landscape orientation
params = {
    "term": "atardecer playa",
    "order": "recent",           # order by most recent
    "page": 1,
    "limit": 5,
    "filters[orientation][landscape]": 1,
    "filters[orientation][portrait]": 0,
    "filters[orientation][square]": 0,
    "filters[orientation][panoramic]": 0,
    "filters[content_type][psd]": 1, # Only PSDs
    "filters[psd][type]": "jpg", # Only JPG PSDs
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
