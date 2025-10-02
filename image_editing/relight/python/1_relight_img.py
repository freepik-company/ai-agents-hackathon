import requests
from dotenv import load_dotenv
import os
import time
import base64

# Load FREEPIK_API_KEY as environment variable from .env file
load_dotenv() 

API_URL = "https://api.freepik.com/v1/ai/image-relight"
timeout = 300 # 5 minutes
generation_ok = True

headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY"), "Content-Type": "application/json"}

IMAGE_URL = "https://img.b2bpic.net/premium-photo/portrait-smiling-senior-woman-blue-vintage-convertible_220770-28364.jpg"
LIGHT_IMAGE_URL = "https://adelaphotography.co.uk/wp-content/uploads/2024/02/Adela-Photography-Petersfield-Hampshire-Wedding-Photographer-Engagement-Photo-Session-Pre-Wedding-Photos-63_websize_2.jpg"
response = requests.get(IMAGE_URL)
if response.status_code == 200:
    print("Image downloaded successfully")
    IMAGE_B64 = base64.b64encode(response.content).decode("utf-8")

payload = {
    "image": IMAGE_B64, # Image to upscale. Only supports base64
    "prompt": "A sunlit forest clearing at golden hour",
    "transfer_light_from_reference_image": LIGHT_IMAGE_URL, # Also supports base64
    #"transfer_light_from_lightmap": LIGHT_IMAGE_URL, # Also supports base64, incompatible with transfer_light_from_reference_image
    "light_transfer_strength": 100, # Possible values: [0,100]
    "interpolate_from_original": False, # Result will be interpolated from the original image.
    "change_background": False, # It will change the background based on your prompt and/or reference image
    "style": "standard", # Possible values: standard, darker_but_realistic, clean, smooth, brighter, contrasted_n_hdr, just_composition
    "preserve_details": True,
    "advanced_settings": {
        "whites": 60, # Adjust the level of white color in the image. Possible values: [0,100]
        "blacks": 60, # Adjust the level of black color in the image. Possible values: [0,100]
        "brightness": 30, # Adjust the level of brightness in the image. Possible values: [0,100]
        "contrast": 40, # Adjust the level of contrast in the image. Possible values: [0,100]
        "saturation": 50, # Adjust the level of saturation in the image. Possible values: [0,100]
        "engine": "automatic", # Possible values: automatic, balanced, cool, real, illusio, fairy, colorful_anime, hard_transform, soft
        "transfer_light_a": "low", # Adjusts the intensity of light transfer. Possible values: automatic, low, medium, normal, high, high_on_faces  
        "transfer_light_b": "soft_in", # Also modifies light transfer intensity. Possible values: automatic, composition, straight, smooth_in, smooth_out, smooth_both, reverse_both, soft_in, soft_out, soft_mid, strong_mid, style_shift, strong_shift
        "fixed_generation": True,
    }
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
        status_url = f"https://api.freepik.com/v1/ai/image-relight/{task_id}"
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
        file_name = os.path.join(current_dir, "relighted_image.jpg")
        image_response = requests.get(IMAGE_URL)
        if image_response.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(image_response.content)
            print(f"Image successfully downloaded as {file_name}")
        else:
            print(f"Could not download the image. Status code: {image_response.status_code}")
else:
    print(f"Error while generating the image. Status code: {response.status_code}, message: {response.json()['message']}")