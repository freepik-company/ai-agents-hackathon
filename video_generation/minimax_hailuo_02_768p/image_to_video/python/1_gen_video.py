import requests
from dotenv import load_dotenv
import os
import time
import base64

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv() 

API_URL = "https://api.freepik.com/v1/ai/image-to-video/minimax-hailuo-02-768p"
timeout = 600 # 10 minutes
generation_ok = True

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

START_FRAME_URL = "https://img.b2bpic.net/premium-photo/portrait-smiling-senior-woman-blue-vintage-convertible_220770-28364.jpg"
END_FRAME_URL = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi9s5NJqu665FVCKamxzvtGpXehW_5YuSsrBHddWPQtRhuaRFQCTwxva1zZs9fuDT-kzKAxeDvhP9_8dZz2lj0gCFJ54dcRCxTneIJWkfQxo14cE3wGeV3pJ51fFrwNs0S_Z_mw8epSqisA/s1600/african_american_rideshare_driver.jpg"

response = requests.get(END_FRAME_URL)
if response.status_code == 200:
    print("Structure reference image downloaded successfully")
    END_FRAME_B64 = base64.b64encode(response.content).decode("utf-8")


payload = {
    "first_frame_image": START_FRAME_URL, # Start frame. Also supports base64
    "last_frame_image": END_FRAME_B64, # End frame. Also supports base64
    "prompt": "An old woman is driving a car and suddenly the camera moves to another car in which a black woman is driving",
    "prompt_optimizer": True, # the model will automatically optimize the incoming prompt
    "duration": "6", # Possible values: 6, 10
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
        status_url = f"https://api.freepik.com/v1/ai/image-to-video/minimax-hailuo-02-768p/{task_id}"
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
else:
    print(f"Error while generating the image. Status code: {response.status_code}, message: {response.json()['message']}")