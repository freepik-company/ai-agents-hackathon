import requests
from dotenv import load_dotenv
import os
import time
import random

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv() 

# 1. Get the style to use randomly from the list of available styles
API_URL = "https://api.freepik.com/v1/ai/loras"
headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY")}

response = requests.get(API_URL, headers=headers)
if response.status_code == 200:
    print("Styles fetched successfully")
    styles = response.json()["data"]
else:
    print(f"Could not fetch styles. Status code: {response.status_code}")

styles_list = styles["default"] # can be "default" or "custom"
style_to_use = random.choice(styles["default"])
print(f"Selected style: {style_to_use['name']}")

# 2. Generate the image
API_URL = "https://api.freepik.com/v1/ai/mystic"

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

payload = {
    "prompt": "a car in the forest",
    "resolution": "2k", # Possible values: 1k, 2k, 4k
    "aspect_ratio": "square_1_1", # Possible values: square_1_1, classic_4_3, traditional_3_4, widescreen_16_9, social_story_9_16, smartphone_horizontal_20_9, smartphone_vertical_9_20, standard_3_2, portrait_2_3, horizontal_2_1, vertical_1_2, social_5_4, social_post_4_5'
    "model": "zen", # Possible values: realism, fluid, zen. More info here https://docs.freepik.com/api-reference/mystic/post-mystic#body-model
    "creative_detailing": 33, # Higher values can achieve greater detail per pixel at higher resolutions at the cost of giving a somewhat more "HDR" or artificial look
    "engine": "automatic", # Possible values: automatic, magnific_illusio, magnific_sharpy, magnific_sparkle. More info here https://docs.freepik.com/api-reference/mystic/post-mystic#body-engine
    "fixed_generation": False, # Fix the generation to the first one
    "filter_nsfw": True, # Filter out NSFW images
    "styling": {
        "styles": [
            {
                "name": style_to_use["name"],
                "strength": 100,
            }
        ],
        "colors": [
            {
                "color": "#F58727",
                "weight": 0.5
            },
            {
                "color": "#2727F5",
                "weight": 0.5
            }
        ]
    }
}
response = requests.post(API_URL, json=payload, headers=headers)

if response.status_code == 200:
    # Active wait until the task is completed

    # Using the API to check the status of the task -----------------------------------
    # Get the task_id from the initial response
    task_id = response.json()["data"]["task_id"]
    status = response.json()["data"]["status"]

    # Polling until the status is "COMPLETED"
    while status != "COMPLETED":
        print(f"Waiting for the task to complete... (current status: {status})")
        time.sleep(2)  # Wait 2 seconds before checking again
        status_url = f"{API_URL}/{task_id}"
        response = requests.get(status_url, headers={"x-freepik-api-key": os.getenv("FREEPIK_API_KEY")})
        if response.status_code == 200:
            status = response.json()["data"]["status"]
        else:
            print(f"Error while checking the task status: {response.status_code}")
            break
    print("COMPLETED")
    # Download the image ---------------------------------------------------------------
    IMG_URL = response.json()["data"]["generated"][0]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(current_dir, "generated_image.jpg")
    img_response = requests.get(IMG_URL)
    if img_response.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(img_response.content)
        print(f"Image successfully downloaded as {file_name}")
    else:
        print(f"Could not download the image. Status code: {img_response.status_code}")