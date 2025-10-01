import requests
from dotenv import load_dotenv
import os
import time

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv() 

API_URL = "https://api.freepik.com/v1/ai/text-to-image/flux-dev"
timeout = 300 # 5 minutes
generation_ok = True

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

payload = {
    "prompt": "a car in the forest",
    #"webhook_url": "https://www.example.com/webhook", # only if you want send the status of the task to a webhook
    "aspect_ratio": "square_1_1", # Possible values: square_1_1, classic_4_3, traditional_3_4, widescreen_16_9, social_story_9_16, standard_3_2, portrait_2_3, horizontal_2_1, vertical_1_2, social_post_4_5
    "styling": {
        "effects": {
            "color": "softhue", # Possible values: softhue, b&w, goldglow, vibrant, coldneon 
            "framing": "portrait", # Possible values: portrait, lowangle, midshot, wideshot, tiltshot, aerial
            "lightning": "iridescent" # Possible values: iridescent, dramatic, goldenhour, longexposure, indorlight, flash, neon
        },
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
    },
    "seed": 2147483648
}

start_time = time.time()
response = requests.post(API_URL, json=payload, headers=headers)
print(response.json())

if response.status_code == 200:
    # Active wait until the task is completed

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
            time.sleep(2)
        if time.time() - start_time > timeout:
            print("Timeout reached")
            generation_ok = False
            break
            
    if generation_ok:
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