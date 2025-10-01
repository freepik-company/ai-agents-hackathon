import os
import requests
from dotenv import load_dotenv

# Load FREEPIK_API_KEY from .env or environment variables
load_dotenv()

API_URL = "https://api.freepik.com/v1/resources"

headers = {
    "x-freepik-api-key": os.getenv("FREEPIK_API_KEY"),
    "Accept-Language": "en-US", # Demonstration with English as default language

}

# Example: search vectors with minimalist style and paginate results
common_params = {
    "term": "minimalist bicicle logo",
    "order": "relevance",
    "limit": 3,
    "filters[content_type][vector]": 1, # Only vectors
    "filters[color]": ["black", "white"],  # uncomment to play with color
}

# Iterate over 2 results pages
for page in (1, 2):
    print(f"\n=== Page {page} ===")
    params = {**common_params, "page": page} # add page number to params
    response = requests.get(API_URL, headers=headers, params=params) # Make the API request
    # Check if the request was successful
    if response.status_code == 200:
        # Iterate over the response data
        for r in response.json()["data"]:
            for k, v in r.items():
                print(f"{k}: {v}")
            print("-"*30)