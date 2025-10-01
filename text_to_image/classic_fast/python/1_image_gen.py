import requests
from dotenv import load_dotenv
import os
import base64

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv() 

API_URL = "https://api.freepik.com/v1/ai/text-to-image"

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

payload = {
    "prompt": "a car in the forest",
    "negative_prompt": "b&w, earth, cartoon, ugly", # Optional
    "guidance_scale": 2,
    "seed": 42,
    "num_images": 1,
    "image": { 
        "size": "square_1_1", # Possible values: square_1_1, classic_4_3, traditional_3_4, widescreen_16_9, social_story_9_16, smartphone_horizontal_20_9, smartphone_vertical_9_20, standard_3_2, portrait_2_3, horizontal_2_1, vertical_1_2, social_5_4, social_post_4_5
    },
    "filter_nsfw": True 
}
response = requests.post(API_URL, json=payload, headers=headers)
if response.status_code == 200:
    print("COMPLETED")
    img_b64 = response.json()["data"][0]["base64"]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(current_dir, "generated_image.jpg")
    with open(file_name, "wb") as f:
        f.write(base64.b64decode(img_b64))
    print(f"Image successfully saved as {file_name}")