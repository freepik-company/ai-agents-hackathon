import os
import requests
from dotenv import load_dotenv

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv() 

# To download a resource, we need to get the RESOURCE_ID from the search results
API_SEARCH_URL = "https://api.freepik.com/v1/resources"

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY")}

# Define the parameters and filters for the API request
params = {
    "term": "old person driving a car", # Search term
    "page": 1, # Results page number
    "limit": 1, # Number of results per page
    "order": "relevance", # Order by relevance, other options: recent
    "filters[orientation][landscape]": 1, # Filter by landscape orientation
    "filters[orientation][portrait]": 0, # Filter by portrait orientation
    "filters[orientation][square]": 1, # Filter by square orientation
    "filters[orientation][panoramic]": 1, # Filter by panoramic orientation
    "filters[content_type][photo]": 1, # Filter by photo content type, other options: vector, psd
    "filters[people][include]": 1, # Include people in the results
    "filters[people][number]": 1, # Number of people in the results
    "filters[people][age]": ["senior", "elder"], # Filter by age, possible values: infant, child, teen, young-adult, adult, senior, elder
    "filters[people][gender]": "female",
    "filters[color]": ["gray", "blue"], # Filter by color, possible values: black, blue, gray, green, orange, red, white, yellow, purple, cyan, pin
    "filters[license][freemium]": 1, # Filter by freemium license
}

# Make the API request
response = requests.get(API_SEARCH_URL, headers=headers, params=params)

if response.status_code == 200:
    # DOWNLOAD API CODE HERE --------------------------------------------------------
    RESOURCE_ID = response.json()["data"][0]["id"]
    API_DOWNLOAD_URL = f"https://api.freepik.com/v1/resources/{RESOURCE_ID}/download"

    params = {
        "image_size": "small", # Possible values: small, medium, large, original
        } 
    response = requests.get(API_DOWNLOAD_URL, headers=headers, params=params)

    if response.status_code == 200:
        url_img = response.json()["data"]["url"]
        if url_img:
            # Save the image in the same directory as this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_name = os.path.join(current_dir, f"{RESOURCE_ID}.jpg")
            img_response = requests.get(url_img)
            if img_response.status_code == 200:
                with open(file_name, "wb") as f:
                    f.write(img_response.content)
                print(f"Image successfully downloaded as {file_name}")
            else:
                print(f"Could not download the image. Status code: {img_response.status_code}")
        else:
            print("Image URL not found in the response.")
    else:
        print(f"Error while downloading the image. Status code: {response.status_code}, message: {response.json()['message']}")
else:
    print(f"Error while searching the image. Status code: {response.status_code}, message: {response.json()['message']}")
