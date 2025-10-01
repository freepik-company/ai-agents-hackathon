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
    "styling": { 
        "style": "anime", # possible values: photo, digital-art, 3d, painting, low-poly, pixel-art, anime, cyberpunk, comic, vintage, cartoon, vector, studio-shot, dark, sketch, mockup, 2000s-pone, 70s-vibe, watercolor, art-nouveau, origami, surreal, fantasy, traditional-japan
        "effects": {
            "color": "pastel",
            "lightning": "warm",
            "framing": "portrait"
        },
        "colors": [ 
            {
                "color": "#FF5733",
                "weight": 1
            },
            {
                "color": "#33FF57",
                "weight": 1
            }
        ]
    },
    "filter_nsfw": True 
}
response = requests.post(API_URL, json=payload, headers=headers)
if response.status_code == 200:
    print("COMPLETED")
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(current_directory, "generated_image.jpg")
    img_b64 = response.json()["data"][0]["base64"]
    with open(file_name, "wb") as f:
        f.write(base64.b64decode(img_b64))
    print(f"Image successfully saved as {file_name}")