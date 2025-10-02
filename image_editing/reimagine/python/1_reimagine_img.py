import requests
from dotenv import load_dotenv
import os
import base64

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv() 

API_URL = "https://api.freepik.com/v1/ai/beta/text-to-image/reimagine-flux"

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

IMAGE_URL = "https://img.b2bpic.net/premium-photo/portrait-smiling-senior-woman-blue-vintage-convertible_220770-28364.jpg"
response = requests.get(IMAGE_URL)
if response.status_code == 200:
    print("Image downloaded successfully")
    IMAGE_B64 = base64.b64encode(response.content).decode("utf-8")

payload = {
    "image": IMAGE_B64, # Image to reimagine. Only supports base64
    "prompt": "an old woman driving a car",
    "imagination": "wild", # imagination level. Possible values: wild, subtle, vivid
    "aspect_ratio": "original", # Possible values: original, square_1_1, classic_4_3, traditional_3_4, widescreen_16_9, social_story_9_16, standard_3_2, portrait_2_3, horizontal_2_1, vertical_1_2, social_post_4_5
    #"webhook_url": "https://www.example.com/webhook", # only if you want send the status of the task to a webhook,
}
response = requests.post(API_URL, json=payload, headers=headers)
if response.status_code == 200:
    print("COMPLETED")
    IMAGE_URL = response.json()["data"]["generated"][0]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(current_dir, "reimagined_image.jpg")
    image_response = requests.get(IMAGE_URL)
    if image_response.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(image_response.content)
        print(f"Image successfully downloaded as {file_name}")
    else:
        print(f"Could not download the image. Status code: {image_response.status_code}")
else:
    print(f"Error while generating the image. Status code: {response.status_code}, message: {response.json()['message']}")