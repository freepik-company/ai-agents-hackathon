import requests
from dotenv import load_dotenv
import os
import time
import base64

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv() 

API_URL = "https://api.freepik.com/v1/ai/gemini-2-5-flash-image-preview"
timeout = 300 # 5 minutes
generation_ok = True

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

IMAGE_REFERENCE_URL = "https://img.b2bpic.net/premium-photo/portrait-smiling-senior-woman-blue-vintage-convertible_220770-28364.jpg"
response = requests.get(IMAGE_REFERENCE_URL)
if response.status_code == 200:
    print("Structure reference image downloaded successfully")
    IMAGE_REFERENCE_B64 = base64.b64encode(response.content).decode("utf-8")

payload = {
    "prompt": "put a the hat in the head of the woman",
    "reference_images": [IMAGE_REFERENCE_B64, "https://shop.rydercup.com/cdn/shop/files/RYDRMH0120_C_2048x.jpg?v=1752179506"],
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