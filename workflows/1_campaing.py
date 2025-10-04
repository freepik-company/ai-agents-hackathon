import os
import requests
from dotenv import load_dotenv
import time
import base64


# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv() 

"""
We are going to create a complete advertising campaing of a red-leather jacket that we haven't seen yet! The idea is to:
- Use a real person because we want the textures as real as we can, for this we'll use the stock.
- As I am not a designer I want an idea for a leather jacket to be commercialized.
- I want both, video and photo advertising to have almost the complete campaing.
"""

# 1. Search and download the image of the model
PROMPT_MODEL = "A young black woman studio photo, full body, she is posing like in a clothes advertising, plain color background"
API_SEARCH_URL = "https://api.freepik.com/v1/resources"
headers =  {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY")}

params = {
    "term": PROMPT_MODEL, 
    "page": 1, 
    "limit": 1, 
}

print("1. Searching for the model image")
search_response = requests.get(API_SEARCH_URL, headers=headers, params=params)
if search_response.status_code == 200:
    # 1.2. Download the image
    RESOURCE_ID = search_response.json()["data"][0]["id"]
    API_DOWNLOAD_URL = f"https://api.freepik.com/v1/resources/{RESOURCE_ID}/download"

    params =dict()
    download_response = requests.get(API_DOWNLOAD_URL, headers=headers, params=params)

    if download_response.status_code == 200:
        MODEL_IMG_URL = download_response.json()["data"]["url"]
    else:
        print(f"Error while downloading the image. Status code: {download_response.status_code}, message: {download_response.json()['message']}") 
        exit()  
else:
    print(f"Error while searching the image. Status code: {search_response.status_code}, message: {search_response.json()['message']}")
    exit()

# TODO - Poner los exosts si algo falla

# 2. Create and download the image of the jacket: We decide to use seedream because we want a wild and creative jacket
PROMPT_JACKET = "A red leather jacket very wild, with many nails but fancy, white and empty background, studio light"
API_URL = "https://api.freepik.com/v1/ai/text-to-image/seedream-v4"
timeout = 300 
generation_ok = True

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

payload = {
    "prompt": PROMPT_JACKET,
    "aspect_ratio": "widescreen_16_9",
    "guidance_scale": 2.5, 
    "seed": 1073741823
}

start_time = time.time()
generation_response = requests.post(API_URL, json=payload, headers=headers)
print("2. Creating the jacket image")
if generation_response.status_code == 200:
    task_id = generation_response.json()["data"]["task_id"]
    status = generation_response.json()["data"]["status"]

    while status != "COMPLETED":
        print(f"Waiting for the task to complete... (current status: {status})")
        time.sleep(2)  # Wait 2 seconds before checking again
        status_url = f"{API_URL}/{task_id}"
        status_response = requests.get(status_url, headers={"x-freepik-api-key": os.getenv("FREEPIK_API_KEY")})
        if status_response.status_code == 200:
            status = status_response.json()["data"]["status"]
        else:
            print(f"Error while checking the task status: {status_response.status_code}")
            time.sleep(2)
        if time.time() - start_time > timeout:
            print("Timeout reached")
            generation_ok = False
            break
            
    if generation_ok:
        print("Jacket generation COMPLETED")
        JACKET_IMG_URL = [u for u in status_response.json()["data"]["generated"] if u.startswith("https://")][0]
else:
    print(f"Error while generating the image. Status code: {generation_response.status_code}, message: {generation_response.json()['message']}")
    exit()

# 3. Upscale the jacket image using Magnific. As the Jacket is invented we'll use the creative Magnific.
PROMPT_UPSCALE_JACKET = PROMPT_JACKET
API_URL = "https://api.freepik.com/v1/ai/image-upscaler"

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

response = requests.get(JACKET_IMG_URL)
if response.status_code == 200:
    print("Image downloaded successfully")
    IMAGE_B64 = base64.b64encode(response.content).decode("utf-8")

payload = {
    "image": IMAGE_B64, 
    "scale_factor": "2x",
    #"optimized_for": "films_n_photography", 
    "prompt": PROMPT_UPSCALE_JACKET, 
    "creativity": 0, 
    "hdr": 0, 
    "resemblance": 0, 
    "fractality": 0, 
    "engine": "automatic", 
}
start_time = time.time()
upscale_response = requests.post(API_URL, json=payload, headers=headers)
print("3. Upscaling the jacket image")
if upscale_response.status_code == 200:
    # Active wait until the task is completed

    # Get the task_id from the initial response
    task_id = upscale_response.json()["data"]["task_id"]
    status = upscale_response.json()["data"]["status"]

    # Polling until the status is "COMPLETED"
    while status != "COMPLETED":
        print(f"Waiting for the task to complete... (current status: {status})")
        time.sleep(2)  # Wait 2 seconds before checking again
        status_url = f"https://api.freepik.com/v1/ai/image-upscaler/{task_id}"
        upscale_response = requests.get(status_url, headers={"x-freepik-api-key": os.getenv("FREEPIK_API_KEY")})
        if upscale_response.status_code == 200:
            status = upscale_response.json()["data"]["status"]
        else:
            print(f"Error while checking the task status: {upscale_response.status_code}")
            time.sleep(2)
        if time.time() - start_time > timeout:
            print("Timeout reached")
            generation_ok = False
            break
            
    if generation_ok:
        print("COMPLETED")
        JACKET_UPSCALED_IMG_URL = upscale_response.json()["data"]["generated"][0]
else:
    print(f"Error while generating the image. Status code: {upscale_response.status_code}, message: {upscale_response.json()['message']}")
    exit()

# 3. Create video's last frame: The idea is that during the video the model will put on the jacket so, the last
#    frame would be the model with the jacket on. As we want to edit the image we'll use Nano Banana. This last frame will be the poster for
#    the campaing so, we'll add some text on it
API_URL = "https://api.freepik.com/v1/ai/gemini-2-5-flash-image-preview"
PROMPT_EDIT = "Put on the jacket in the woman, change the pose of the woman, she should be smiling, this will be an advertisement poster, add the text 'I'm happy in red', do not change the background"

timeout = 300
generation_ok = True

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

payload = {
    "prompt": PROMPT_EDIT,
    "reference_images": [MODEL_IMG_URL, JACKET_IMG_URL],
}

start_time = time.time()
edit_response = requests.post(API_URL, json=payload, headers=headers)
print("4. Editing the jacket")
if edit_response.status_code == 200:
    task_id = edit_response.json()["data"]["task_id"]
    status = edit_response.json()["data"]["status"]

    while status != "COMPLETED":
        print(f"Waiting for the task to complete... (current status: {status})")
        time.sleep(2)  # Wait 2 seconds before checking again
        status_url = f"{API_URL}/{task_id}"
        status_response = requests.get(status_url, headers={"x-freepik-api-key": os.getenv("FREEPIK_API_KEY")})
        if status_response.status_code == 200:
            status = status_response.json()["data"]["status"]
        else:
            print(f"Error while checking the task status: {status_response.status_code}")
            time.sleep(2)
        if time.time() - start_time > timeout:
            print("Timeout reached")
            generation_ok = False
            break
            
    if generation_ok:
        MODEL_JACKET_IMG_URL = [u for u in status_response.json()["data"]["generated"] if u.startswith("https://")][0] # We need to filter out the urls that don't start with https://
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(current_dir, "poster_image.jpg")
        image_response = requests.get(MODEL_JACKET_IMG_URL)
        if image_response.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(image_response.content)
            print(f"Image successfully downloaded as {file_name}")
else:
    print(f"Error while generating the image. Status code: {status_response.status_code}, message: {status_response.json()['message']}")
    exit()

# 4. Create the video using the first and last frames: We are using Kling v2.1 pro
API_URL = "https://api.freepik.com/v1/ai/image-to-video/kling-v2-1-pro"
PROMPT_VIDEO = "An advertisement of a red leather jacket, in the video a black woman model puts on the jacket and some letters appear, the video has a happy atmosphere and it is dynamic"

timeout = 600
generation_ok = True

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

payload = {
    "image": MODEL_IMG_URL,
    "image_tail": MODEL_JACKET_IMG_URL, # End framee. Also supports URL
    "prompt": PROMPT_VIDEO,
    "negative_prompt": "ugly, cartoon, b&w, earth, ugly",
    "duration": "5",
    "cfg_scale": 0.5,
}
start_time = time.time()
generation_response = requests.post(API_URL, json=payload, headers=headers)
print("5. Creating the video")
if generation_response.status_code == 200:
    # Active wait until the task is completed

    # Get the task_id from the initial response
    task_id = generation_response.json()["data"]["task_id"]
    status = generation_response.json()["data"]["status"]

    # Polling until the status is "COMPLETED"
    while status != "COMPLETED":
        print(f"Waiting for the task to complete... (current status: {status})")
        time.sleep(2)  # Wait 2 seconds before checking again
        status_url = f"https://api.freepik.com/v1/ai/image-to-video/kling-v2-1/{task_id}"
        generation_response = requests.get(status_url, headers={"x-freepik-api-key": os.getenv("FREEPIK_API_KEY")})
        if generation_response.status_code == 200:
            status = generation_response.json()["data"]["status"]
        else:
            print(f"Error while checking the task status: {generation_response.status_code}")
            time.sleep(2)
        if time.time() - start_time > timeout:
            print("Timeout reached")
            generation_ok = False
            break
            
    if generation_ok:
        print("Video generation COMPLETED")
        VIDEO_URL = generation_response.json()["data"]["generated"][0]
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(current_dir, "generated_video.mp4")
        generation_response = requests.get(VIDEO_URL)
        if generation_response.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(generation_response.content)
            print(f"Video successfully downloaded as {file_name}")
        else:
            print(f"Could not download the video. Status code: {generation_response.status_code}")
else:
    print(f"Error while generating the image. Status code: {generation_response.status_code}, message: {generation_response.json()['message']}")
    exit()