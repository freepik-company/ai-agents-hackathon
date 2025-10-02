import requests
from dotenv import load_dotenv
import os
import time
import base64

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv() 

API_URL = "https://api.freepik.com/v1/ai/mystic"
timeout = 300 # 5 minutes
generation_ok = True

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

STYLE_REFERENCE_URL = "https://img.b2bpic.net/premium-photo/portrait-smiling-senior-woman-blue-vintage-convertible_220770-28364.jpg"
response = requests.get(STYLE_REFERENCE_URL)
if response.status_code == 200:
    print("Style reference image downloaded successfully")
    STYLE_REFERENCE_B64 = base64.b64encode(response.content).decode("utf-8")
    payload = {
        "prompt": "a car in the forest",
        "style_reference": STYLE_REFERENCE_B64,
        "adherence": 50, # Increasing this value will make your generation more faithful to the prompt, but it may transfer the style a bit less accurately.
        "hdr": 50, # ncreasing this value can give you a more detailed image, at the cost of a more 'AI look' and slightly worse style transfer
        "resolution": "1k", # Possible values: 1k, 2k, 4k
        "aspect_ratio": "square_1_1", # Possible values: square_1_1, classic_4_3, traditional_3_4, widescreen_16_9, social_story_9_16, smartphone_horizontal_20_9, smartphone_vertical_9_20, standard_3_2, portrait_2_3, horizontal_2_1, vertical_1_2, social_5_4, social_post_4_5'
        "model": "realism", # Possible values: realism, fluid, zen. More info here https://docs.freepik.com/api-reference/mystic/post-mystic#body-model
        "creative_detailing": 33, # Higher values can achieve greater detail per pixel at higher resolutions at the cost of giving a somewhat more "HDR" or artificial look
        "engine": "automatic", # Possible values: automatic, magnific_illusio, magnific_sharpy, magnific_sparkle. More info here https://docs.freepik.com/api-reference/mystic/post-mystic#body-engine
        "fixed_generation": False, # Fix the generation to the first one
        "filter_nsfw": True, # Filter out NSFW images
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
else:
    print(f"Error while generating the image. Status code: {response.status_code}, message: {response.json()['message']}")