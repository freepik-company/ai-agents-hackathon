import requests
from dotenv import load_dotenv
import os
import time
import base64

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv() 

API_URL = "https://api.freepik.com/v1/ai/image-style-transfer"
timeout = 300 # 5 minutes
generation_ok = True

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

IMAGE_URL = "https://img.b2bpic.net/premium-photo/portrait-smiling-senior-woman-blue-vintage-convertible_220770-28364.jpg"
REF_IMAGE_URL = "https://static.toiimg.com/thumb/msid-121340289,imgsize-74920,width-400,resizemode-4/the-first-episode-of-demon-slayer-kimetsu-no-yaiba.jpg"
response = requests.get(REF_IMAGE_URL)
if response.status_code == 200:
    print("Style reference image downloaded successfully")
    REF_IMAGE_B64 = base64.b64encode(response.content).decode("utf-8")

payload = {
    "image": IMAGE_URL, # Image to style. Also supports base64
    "reference_image": REF_IMAGE_B64, # Style reference image. Also supports URL
    "prompt": "An old woman is driving a car and suddenly the camera moves to another car in which a black woman is driving",
    "style_strength": 85, # Possible values: [0,100]
    "structure_strength": 100, # Possible values: [0,100]
    "is_portrait": True, # Possible values: True, False
    "portrait_ratio": "standard", # Possible values: standard, pop, super_pop
    "portrait_beautifier": "beautify_face", # Enable facial beutification. Possible values: beautify_face, beautify_face_max
    "flavor": "clear", # Possible values: faithful, gen_z, psychedelia, detaily, clear, donotstyle, donotstyle_sharp 
    "engine": "balanced", # Possible values: balanced, definio, illusio, 3d_cartoon, colorful_anime, caricature, real, super_real, softy 
    "fixed_generation": False, # Possible values: True, False
    #"webhook_url": "https://www.example.com/webhook", # only if you want send the status of the task to a webhook,

}
start_time = time.time()
response = requests.post(API_URL, json=payload, headers=headers)
if response.status_code == 200:
    # Active wait until the task is completed
    # Get the task_id from the initial response
    task_id = response.json()["task_id"]
    status = response.json()["task_status"]

    # Polling until the status is "COMPLETED"
    while status != "COMPLETED":
        print(f"Waiting for the task to complete... (current status: {status})")
        time.sleep(2)  # Wait 2 seconds before checking again
        status_url = f"https://api.freepik.com/v1/ai/image-style-transfer/{task_id}"
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
        IMAGE_URL = response.json()["data"]["generated"][0]
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(current_dir, "styled_image.jpg")
        image_response = requests.get(IMAGE_URL)
        if image_response.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(image_response.content)
            print(f"Image successfully downloaded as {file_name}")
        else:
            print(f"Could not download the image. Status code: {image_response.status_code}")
else:
    print(f"Error while generating the image. Status code: {response.status_code}, message: {response.json()['message']}")