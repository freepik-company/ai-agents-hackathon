import requests
from dotenv import load_dotenv
import os
import time

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv() 

API_URL = "https://api.freepik.com/v1/ai/text-to-image/seedream-v4"
timeout = 300 # 5 minutes
generation_ok = True

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

payload = {
    "prompt": "a car in the forest",
    "aspect_ratio": "square_1_1", # Possible values: square_1_1, widescreen_16_9, social_story_9_16, portrait_2_3, traditional_3_4, standard_3_2, classic_4_3
    "guidance_scale": 2.5, # Possible values: 0 <= x <= 20
    "seed": 1073741823
    #"webhook_url": "https://www.example.com/webhook", # only if you want send the status of the task to a webhook,
}

start_time = time.time()
response = requests.post(API_URL, json=payload, headers=headers)

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
        IMG_URL = [u for u in response.json()["data"]["generated"] if u.startswith("https://")][0] # We need to filter out the urls that don't start with https://
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(current_dir, "generated_image.jpg")
        img_response = requests.get(IMG_URL)
        if img_response.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(img_response.content)
            print(f"Image successfully downloaded as {file_name}")
        else:
            print(f"Could not download the image. Status code: {img_response.status_code}")
else:
    print(f"Error while generating the image. Status code: {response.status_code}, message: {response.json()['message']}")