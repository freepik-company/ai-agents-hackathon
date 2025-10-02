import requests
from dotenv import load_dotenv
import os
import time
import base64

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv() 

API_URL = "https://api.freepik.com/v1/ai/image-upscaler"
timeout = 300 # 5 minutes
generation_ok = True

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

IMAGE_URL = "https://img.b2bpic.net/premium-photo/portrait-smiling-senior-woman-blue-vintage-convertible_220770-28364.jpg"

response = requests.get(IMAGE_URL)
if response.status_code == 200:
    print("Image downloaded successfully")
    IMAGE_B64 = base64.b64encode(response.content).decode("utf-8")

payload = {
    "image": IMAGE_B64, # Image to upscale. Only supports base64
    "scale_factor": "4x", # Possible values: 2x, 4x, 8x, 16x
    "optimized_for": "standard", # Styles to optimize the upscale process. Possible values: standard, soft_portraits, hard_portraits, art_n_illustration, videogame_assets, nature_n_landscapes, films_n_photography, 3d_renders, science_fiction_n_horror
    "prompt": "An old woman is driving a car", # Reusing the same prompt for AI-generated images will improve the results
    "creativity": 0, # Increase or decrease AI's creativity. Possible values: [-10,10]
    "hdr": 0, # Increase or decrease the level of definition and detail. Possible values: [-10,10]
    "resemblance": 0, # Adjust the level of resemblance to the original image. Possible values: [-10,10]
    "fractality": 0, # Control the strength of the prompt. Possible values: [-10,10]
    "engine": "magnific_sparkle", # Different magnific flavours. Possible values: automatic, magnific_illusio, magnific_sharpy, magnific_sparkle
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
        # Download the video ---------------------------------------------------------------
        IMAGE_URL = response.json()["data"]["generated"][0]
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(current_dir, "upscaled_image.jpg")
        image_response = requests.get(IMAGE_URL)
        if image_response.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(image_response.content)
            print(f"Image successfully downloaded as {file_name}")
        else:
            print(f"Could not download the image. Status code: {image_response.status_code}")
else:
    print(f"Error while generating the image. Status code: {response.status_code}, message: {response.json()['message']}")