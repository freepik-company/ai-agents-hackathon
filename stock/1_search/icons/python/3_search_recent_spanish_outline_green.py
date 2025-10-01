import os
import requests
from dotenv import load_dotenv

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv()

API_URL = "https://api.freepik.com/v1/icons"

headers = {
    "x-freepik-api-key": os.getenv("FREEPIK_API_KEY"),
    "Accept-Language": "es-ES",  # Force Spanish language in search
}

# Define parameters and filters for a recent search in Spanish
params = {
    "term": "amor",  # Search term
    "page": 1,  # Results page number
    "per_page": 5,  # Results per page
    "order": "recent",  # Order by recent
    "thumbnail_size": 256,  # Thumbnail size (default 128)
    "filters[free_svg]": ["free"],
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

