import os
import requests
from dotenv import load_dotenv


# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv()

API_URL = "https://api.freepik.com/v1/videos"

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"),}

common_params = {
    "term": "city street portrait",  # Required search term
    "page": 1,
    "order": "relevance",
    #"filters[orientation]": ["vertical", "square"],
    "filters[ai-generated][excluded]": 0,
    "filters[ai-generated][only]": 1,
}

for page in range(1, 3):
    print(f"\n=== Page {page} ===")
    params = {**common_params, "page": page}
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
