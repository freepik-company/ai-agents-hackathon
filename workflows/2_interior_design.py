

"""
the main idea is to create a interior desing for a living room.
As we don't have a real living room we'll use the stock to create a living room.
Then we'll create some furniture for the living room.
Then we'll put the furniture in the living room.
Finall we'll create like a house tour video with the living room.
"""

import requests
from dotenv import load_dotenv
import os
import time
import base64

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv() 

# 1. Generate the room
print("1. Generating the room")
PROMPT_ROOM = "A very cozy living room with no furniture, just a wall with a window and a floor with a carpet, maybe there is a fireplace"
API_URL = "https://api.freepik.com/v1/ai/text-to-image/imagen3"
timeout = 300
generation_ok = True

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

payload = {
    "prompt": PROMPT_ROOM,
    "num_images": 1,
    "aspect_ratio": "square_1_1",
}

start_time = time.time()
response = requests.post(API_URL, json=payload, headers=headers)
print(response.json())

if response.status_code == 200:
    task_id = response.json()["data"]["task_id"]
    status = response.json()["data"]["status"]
    while status != "COMPLETED":
        print(f"Waiting for the task to complete... (current status: {status})")
        time.sleep(2)
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
        ROOM_URL = response.json()["data"]["generated"][0]
else:
    print(f"Error while generating the image. Status code: {response.status_code}, message: {response.json()['message']}")

# 2. Generate the furnitures according to the room
print("2. Generating the furnitures")
API_URL = "https://api.freepik.com/v1/ai/mystic"
headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}
timeout = 300 # 5 minutes
generation_ok = True

PROMPT_FURNITURES = ["A big sofa", "A table", "A chair", "A lamp", "A plant"]
STYLE_REFERENCE_URL = ROOM_URL
response = requests.get(STYLE_REFERENCE_URL)
if response.status_code == 200:
    print("Style reference image downloaded successfully")
    STYLE_REFERENCE_B64 = base64.b64encode(response.content).decode("utf-8")

furnitures_urls = []
for PROMPT_FURNITURE in PROMPT_FURNITURES:
    PROMPT_FURNITURE = f"{PROMPT_FURNITURE} in completely white background, studio shot"
    payload = {
        "prompt": PROMPT_FURNITURE,
        "style_reference": STYLE_REFERENCE_B64,
        "adherence": 50,
        "hdr": 50,
        "resolution": "1k",
        "aspect_ratio": "square_1_1",
        "model": "realism",
        "creative_detailing": 33,
        "engine": "automatic",
        "fixed_generation": False,
        "filter_nsfw": True,
    }
    headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY")}
    
    start_time = time.time()
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
                time.sleep(2)
            if time.time() - start_time > timeout:
                print("Timeout reached")
                generation_ok = False
                break
                
        if generation_ok:
            print("COMPLETED")
            URL = response.json()["data"]["generated"][0]
            furnitures_urls.append(URL)
    else:
        print(f"Error while generating the image. Status code: {response.status_code}, message: {response.json()['message']}")

# 3. Put the furnitures in the room
print("3. Putting the furnitures in the room")
API_URL = "https://api.freepik.com/v1/ai/gemini-2-5-flash-image-preview"
timeout = 300 # 5 minutes
generation_ok = True
PROMPT_EDIT = "put the furniture in the room in a realistic way, make a design of the room to have a nice look, feng shui style"

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

for FURNITURE_URL in furnitures_urls:
    payload = {
        "prompt": PROMPT_EDIT,
        "reference_images": [ROOM_URL, FURNITURE_URL],
    }
    start_time = time.time()
    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        task_id = response.json()["data"]["task_id"]
        status = response.json()["data"]["status"]
        while status != "COMPLETED":
            print(f"Waiting for the task to complete... (current status: {status})")
            time.sleep(2)  # Wait 2 seconds before checking again
            status_url = f"{API_URL}/{task_id}"
            response = requests.get(status_url, headers={"x-freepik-api-key": os.getenv("FREEPIK_API_KEY")})
            if response.status_code == 200:
                status = response.json()["data"]["status"]
            elif response.status_code == 400:
                print(f"Error while generating the image. Status code: {response.status_code}, message: {response.json()['message']}")
                generation_ok = False
                break
            else:
                print(f"Error while checking the task status: {response.status_code}")
                time.sleep(2)
            if time.time() - start_time > timeout:
                print("Timeout reached")
                generation_ok = False
                break
                
        if generation_ok:
            print("COMPLETED")
            ROOM_URL = [u for u in response.json()["data"]["generated"] if u.startswith("https://")][0] # We need to filter out the urls that don't start with https://
            print(f"Room full URL: {ROOM_URL}")
    else:
        print(f"Error while generating the image. Status code: {response.status_code}, message: {response.json()['message']}")
        exit()

# 4. Upscale the full room image
print("4. Upscaling the full room image")
PROMPT_UPSCALE = "A very cozy living room with furniture, realistic, nice look, feng shui style"
API_URL = "https://api.freepik.com/v1/ai/image-upscaler"
timeout = 300
generation_ok = True

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

response = requests.get(ROOM_URL)
if response.status_code == 200:
    print("Image downloaded successfully")
    IMAGE_B64 = base64.b64encode(response.content).decode("utf-8")

payload = {
    "image": IMAGE_B64,
    "scale_factor": "2x",
    "optimized_for": "standard",
    "prompt": PROMPT_UPSCALE,
    "creativity": 0,
    "hdr": 0,
    "resemblance": 0,
    "fractality": 0,
    "engine": "magnific_sparkle",
}
start_time = time.time()
response = requests.post(API_URL, json=payload, headers=headers)
if response.status_code == 200:
    task_id = response.json()["data"]["task_id"]
    status = response.json()["data"]["status"]
    # Polling until the status is "COMPLETED"
    while status != "COMPLETED":
        print(f"Waiting for the task to complete... (current status: {status})")
        time.sleep(2)  # Wait 2 seconds before checking again
        status_url = f"https://api.freepik.com/v1/ai/image-upscaler/{task_id}"
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
        FULL_ROOM_UPSCALED_URL = response.json()["data"]["generated"][0]
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(current_dir, "full_room_upscaled.jpg")
        image_response = requests.get(FULL_ROOM_UPSCALED_URL)
        if image_response.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(image_response.content)
            print(f"Image successfully downloaded as {file_name}")
        else:
            print(f"Could not download the image. Status code: {image_response.status_code}")
else:
    print(f"Error while generating the image. Status code: {response.status_code}, message: {response.json()['message']}")

# 4. Create a video of the house tour
print("5. Creating the video of the house tour")
PROMPT_VIDEO = "A video of a house tour, showing the living room with the furniture and the design, ready for a platform like instagram, the camera moves along all the room showing all the details"
API_URL = "https://api.freepik.com/v1/ai/image-to-video/kling-v2"
timeout = 600 # 10 minutes
generation_ok = True

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

payload = {
    "image": FULL_ROOM_UPSCALED_URL, # Start frame. Also supports base64
    "prompt": PROMPT_VIDEO,
    "negative_prompt": "ugly, cartoon, b&w, earth, ugly",
    "duration": "5",
    "cfg_scale": 0.5,
}
start_time = time.time()
response = requests.post(API_URL, json=payload, headers=headers)
if response.status_code == 200:
    task_id = response.json()["data"]["task_id"]
    status = response.json()["data"]["status"]
    while status != "COMPLETED":
        print(f"Waiting for the task to complete... (current status: {status})")
        time.sleep(2)  # Wait 2 seconds before checking again
        status_url = f"https://api.freepik.com/v1/ai/image-to-video/kling-v2/{task_id}"
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
        VIDEO_URL = response.json()["data"]["generated"][0]
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(current_dir, "house_tour.mp4")
        video_response = requests.get(VIDEO_URL)
        if video_response.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(video_response.content)
            print(f"Video successfully downloaded as {file_name}")
        else:
            print(f"Could not download the video. Status code: {video_response.status_code}")
else:
    print(f"Error while generating the image. Status code: {response.status_code}, message: {response.json()['message']}")