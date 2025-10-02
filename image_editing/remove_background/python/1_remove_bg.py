import requests
from dotenv import load_dotenv
import os
import time

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv() 

API_URL = "https://api.freepik.com/v1/ai/beta/remove-background"
timeout = 300 # 5 minutes
generation_ok = True

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/x-www-form-urlencoded"}

IMAGE_URL = "https://img.b2bpic.net/premium-photo/portrait-smiling-senior-woman-blue-vintage-convertible_220770-28364.jpg"

payload = {
    "image_url": IMAGE_URL, # Image to remove the BG. Only supports URL
}

start_time = time.time()
response = requests.post(API_URL, data=payload, headers=headers)
if response.status_code == 200:
    IMAGE_URL = response.json()["high_resolution"]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(current_dir, "removed_bg_image.jpg")
    image_response = requests.get(IMAGE_URL)
    if image_response.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(image_response.content)
        print(f"Image successfully downloaded as {file_name}")
    else:
        print(f"Could not download the image. Status code: {image_response.status_code}")
else:
    print(f"Error while generating the image. Status code: {response.status_code}, message: {response.json()['message']}")