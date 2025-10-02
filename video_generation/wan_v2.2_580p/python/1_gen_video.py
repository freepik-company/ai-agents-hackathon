import requests
from dotenv import load_dotenv
import os
import time

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv() 

API_URL = "https://api.freepik.com/v1/ai/image-to-video/wan-v2-2-580p"
timeout = 600 # 10 minutes
generation_ok = True

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

START_FRAME_URL = "https://img.b2bpic.net/premium-photo/portrait-smiling-senior-woman-blue-vintage-convertible_220770-28364.jpg"

payload = {
    "prompt": "An old woman is driving a car and suddenly the camera moves to another car in which a black woman is driving",
    "image": START_FRAME_URL, # Start frame. Also supports base64
    "duration": "5", # Possible values: 5, 10
    "aspect_ratio": "auto", # Possible values: auto, widescreen_16_9, social_story_9_16, square_1_1, classic_4_3
    "seed": 42,
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
        status_url = f"https://api.freepik.com/v1/ai/image-to-video/wan-v2-2-480p/{task_id}"
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
        # Download the video ---------------------------------------------------------------
        VIDEO_URL = response.json()["data"]["generated"][0]
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(current_dir, "generated_video.mp4")
        video_response = requests.get(VIDEO_URL)
        if video_response.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(video_response.content)
            print(f"Video successfully downloaded as {file_name}")
        else:
            print(f"Could not download the video. Status code: {video_response.status_code}")