import os
import requests
from dotenv import load_dotenv

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv() 

API_URL = "https://api.freepik.com/v1/resources"

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY")}

# Define the parameters and filters for the API request
params = {
    "term": "old person driving a car", # Search term
    "page": 1, # Results page number
    "limit": 5, # Number of results per page
    "order": "relevance", # Order by relevance, other options: recent
    "filters[orientation][landscape]": 1, # Filter by landscape orientation
    "filters[orientation][portrait]": 0, # Filter by portrait orientation
    "filters[orientation][square]": 1, # Filter by square orientation
    "filters[orientation][panoramic]": 1, # Filter by panoramic orientation
    "filters[content_type][photo]": 1, # Filter by photo content type, other options: vector, psd
    "filters[people][include]": 1, # include people in the results
    "filters[people][number]": 1, # number of people in the results
    "filters[people][age]": ["senior", "elder"], # filter by age, possible values: infant, child, teen, young-adult, adult, senior, elder
    "filters[people][gender]": "female",
    "filters[color]": ["gray", "blue"], # filter by color, possible values: black, blue, gray, green, orange, red, white, yellow, purple, cyan, pin
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

