# Freepik API

Hi!

We've created this repo with a lot of examples of how to use the different tools available in the Freepik API. As there are many different tools it could be hard to find the one you need, so in this README you'll find a summary of the tools available organized by use case and and highlighting how different each of the tools is.

## Installation

### Python

Create a virtual environment and install the dependencies:
```bash
python -m venv <path-to-your-virtual-environment>
source <path-to-your-virtual-environment>/bin/activate
pip install -r requirements.txt
```

To run the examples you need to have the API key set up. To do that you have to create a `.env` file in the root of the project and add the API key to it with this format:
```
FREEPIK_API_KEY=<your_api_key>
```

### Curl

To run the curl examples you will need to export the API key to the environment variable by running this command in the terminal:
```bash
export FREEPIK_API_KEY=<your_api_key>
```

## Image tools

### Stock resources

Freepik offers a wide range of stock resources, including images, icons and templates. Using the API you can search for resources and download them.

<details>
<summary><b>Search resources tools</b></summary>

| Tool | Description | Links|
|------|-------------|------|
| Images and templates | Search for images and templates | [Docs](https://docs.freepik.com/api-reference/resources/get-all-resources) - [Python examples](stock/1_search/images_and_templates/python) - [Curl examples](stock/1_search/images_and_templates/curl)|

</details>

<details>
<summary><b>Download resources tools</b></summary>

| Tool | Description | Links|
|------|-------------|------|
| Download image and template | Download an image or a template by its id | [Docs](https://docs.freepik.com/api-reference/resources/download-a-resource) - [Python examples](stock/2_download/images_and_templates/python) - [Curl examples](stock/2_download/images_and_templates/curl)|
| Download icon | Download an icon by its id | [Docs](https://docs.freepik.com/api-reference/icons/download-icon-by-id) - [Python examples](stock/2_download/icons/python) - [Curl examples](stock/2_download/icons/curl)|

</details>


### Text to image generation

Freepik offers a wide range of text to image tools, including classic fast, flux dev, and more. Using the API you can generate images from text. In the table below you'll find a summary of the tools available and how they differ from each other.

<details>
<summary><b>Text to image generation tools</b></summary>

| Tool | Description | Important differences | Links|
|------|-------------|------------------------|------|
| Classic fast | Generates images from text using the classic fast model. | It is synchronous and returns the image very fast. It also allows you to add style, effects and colors to the image.| [Docs](https://docs.freepik.com/api-reference/text-to-image/get-image-from-text) - [Python examples](text_to_image/classic_fast/python) - [Curl examples](text_to_image/classic_fast/curl)|
| Flux dev | Generates images from text using the flux dev model. | It allows you to add style, effects and colors to the image. It has good prompt adherence. It is asynchronous. | [Docs](https://docs.freepik.com/api-reference/text-to-image/flux-dev/post-flux-dev) - [Python examples](text_to_image/flux_dev/python)|
| Flux pro v1.1 | Generates images from text using the flux pro v1.1 model. | Pure precision. It is asynchronous. | [Docs](https://docs.freepik.com/api-reference/text-to-image/flux-pro-v1-1/post-flux-pro-v1-1) - [Python example](text_to_image/flux_proV1.1/python)|
| Hyperflux | Another flavour of flux model that generates only in 8 steps. | It allows you to add style, effects and colors to the image. It is asynchronous. | [Docs](https://docs.freepik.com/api-reference/text-to-image/hyperflux/post-hyperflux) - [Python examples](text_to_image/hyperFlux/python)|
| Mystic | Generates 2K images from text. | Add style and colors to the image. Add a style reference image and a structure reference image. Generate directly in 1K, 2K or 4K resolution. Select output aspect ratio. It is asynchronous. | [Docs](https://docs.freepik.com/api-reference/mystic/mystic) - [Python examples](text_to_image/mystic/python)|
| Google Imagen 3 | High quality images from text. | It allows you to add style and colors to the image. It has many moderation options. It is asynchronous. | [Docs](https://docs.freepik.com/api-reference/text-to-image/imagen3/post-imagen3) - [Python examples](text_to_image/google_imagen3/python)|
| Seedream | Generates more creative and aesthetics images | Select output aspect ratio. It is asynchronous. | [Docs](https://docs.freepik.com/api-reference/text-to-image/seedream/post-seedream) - [Python example](text_to_image/seedream/python)|
| Seedream 4 | Generates more creative and aesthetics images | Select output aspect ratio. It is asynchronous. | [Docs](https://docs.freepik.com/api-reference/text-to-image/seedream-v4/post-seedream-v4) - [Python example](text_to_image/seedream4/python)|
</details>

<details>
<summary><b>Text to image generation and editing tools</b></summary>

You can use reference images to edit them or to generate new images from them.

| Tool | Description | Important differences | Links|
|------|-------------|------------------------|------|
| Seedream 4 edit | Edit an image using a reference image or generate a new image from a reference images | Select output aspect ratio. Can use multiple reference images. Can edit a given image based on another reference image. It is asynchronous. | [Docs](https://docs.freepik.com/api-reference/text-to-image/seedream-v4-edit/post-seedream-v4-edit) - [Python example](text_to_image/seedream4_edit/python)|
| Google Nano Banana | Edit an image using a reference image or generate a new image from a reference images | Can use multiple reference images. Can edit a given image based on another reference image. It is asynchronous. | [Docs](https://docs.freepik.com/api-reference/text-to-image/google/gemini-2-5-flash-image-preview) - [Python example](text_to_image/gemini2.5_flash/python)|
</details>

### Image Editing

There are many tools to edit images, including style transfer, reimagine, and more. Using the API you can edit images. 

<details>
<summary><b>Image editing tools</b></summary>

| Tool | Description | Important differences | Links|
|------|-------------|------------------------|------|
| Magnific creative | Upscale an image using a reference image in a creative way | Upscale an image to 4x, 8x or 16x resolution. It is creative what means it can change the image in a creative way by adding details and improving the image. It is asynchronous. | [Docs](https://docs.freepik.com/api-reference/image-upscaler-creative/image-upscaler) - [Python example](image_editing/upscaler/magnific_creative/python)|
| Magnific precision | Upscale an image using a reference image in a non creative way | It doesn't make up anything, pure precision. You can add grain to make the result more realistic. Can modify the sharpening. It is asynchronous. | [Docs](https://docs.freepik.com/api-reference/image-upscaler-precision/image-upscaler) - [Python example](image_editing/upscaler/magnific_precision/python)|
| Remove Background | Remove the background of an image | It is synchronous. | [Docs](https://docs.freepik.com/api-reference/remove-background/post-beta-remove-background) - [Python example](image_editing/remove_background/python)|
| Image expand | Expand an image from the current size to a bigger size| It is asynchronous. | [Docs](https://docs.freepik.com/api-reference/image-expand/get-flux-pro) - [Python example](image_editing/image_expand/python)|
| Style transfer | Transfer the style of a reference image to an image | Use an image as style reference. Control the influence of the style adn the influence of the structure. It is asynchronous.| [Docs](https://docs.freepik.com/api-reference/image-style-transfer/image-styletransfer) - [Python example](image_editing/style_transfer/python)|
| Relight | Relighing an image using a reference image and a prompt | Use an image or/and a prompt as light reference. Control the influence of the light. Control many other parameters of the generation. Apply some predefinied styles. It is asynchronous.| [Docs](https://docs.freepik.com/api-reference/image-relight/image-relight) - [Python example](image_editing/relight/python)|
| Reimagine | Create variations of a reference image | Control the variatioon level. Control the aspect ratio. It is synchronous.| [Docs](https://docs.freepik.com/api-reference/image-reimagine/post-image-reimagine) - [Python example](https://docs.freepik.com/api-reference/text-to-image/reimagine-flux/post-reimagine-flux)|
</details>

## Video tools

### Stock resources

Freepik offers a wide range of stock video. Using the API you can search for resources and download them.

<details>
<summary><b>Search resources tools</b></summary>

| Tool | Description | Links|
|------|-------------|------|
| Videos | Search for videos | [Docs](https://docs.freepik.com/api-reference/videos/get-all-videos-by-order) - [Python examples](stock/1_search/videos/python) - [Curl examples](stock/1_search/videos/curl)|
</details>
  
<details>
<summary><b>Download resources tools</b></summary>

| Tool | Description | Links|
|------|-------------|------|
| Download video | Download a video by its id | [Docs](https://docs.freepik.com/api-reference/videos/download-video-by-id) - [Python examples](stock/2_download/videos/python) - [Curl examples](stock/2_download/videos/curl)|

</details>

### Video generation

Freepik offers a wide range of video generation tools, including kling, seedance, and more. Using the API you can generate videos from images or text.

<details>
<summary><b>Image to video generation tools</b></summary>

All of them are asynchronous.

__First and last frame conditioning__

| Tool | Important differences | Links|
|------|------------------------|------|
|Kling v1.6 pro | Negative prompt to improve quality. | [Docs](https://docs.freepik.com/api-reference/image-to-video/kling-pro/post-kling-pro) - [Python example](video_generation/kling_v1.6_pro/python/1_gen_video.py)|

|Kling v2.1 pro | Negative prompt to improve quality. Better quality than 2 | [Docs](https://docs.freepik.com/api-reference/image-to-video/kling-v2.1-pro/overview) - [Python example](video_generation/kling_v2.1_pro/python/1_gen_video.py)|

|Pixverse v5 transition | Can generate different resolutions. Can apply some predefinied styles. Negative prompt to improve quality.| [Docs](https://docs.freepik.com/api-reference/image-to-video/pixverse-transition/post-pixverse-v5-transition) - [Python example](video_generation/pixverse_v5_transition/python/1_gen_video.py)|

|Minimax Hailuo 02 768p| It has automatic prompt optimizer. Resolution 768p. |[Docs](https://docs.freepik.com/api-reference/image-to-video/minimax-hailuo-02-768p/post-minimax-hailuo-02-768p) - [Python example](video_generation/minimax_hailuo_02_768p/image_to_video/python/1_gen_video.py)|

|Minimax Hailuo 02 1080p| It has automatic prompt optimizer. Resolution 1080p.|[Docs](https://docs.freepik.com/api-reference/image-to-video/minimax-hailuo-02-1080p/post-minimax-hailuo-02-1080p) - [Python example](video_generation/minimax_hailuo_02_1080p/image_to_video/python/1_gen_video.py)|


__Only first frame conditioning__

| Tool | Important differences | Links|
|------|------------------------|------|
|Kling v1.6 std | Negative prompt to improve quality. | [Docs](https://docs.freepik.com/api-reference/image-to-video/kling-std/post-kling-std) - [Python example](video_generation/kling_v1.6_std/python/1_gen_video.py)|

|Kling v2 | Negative prompt to improve quality. Better quality than 1.6 | [Docs](https://docs.freepik.com/api-reference/image-to-video/kling-v2/post-kling-v2) - [Python example](video_generation/kling_v2/python/1_gen_video.py)|

|Kling v2.1 master | Negative prompt to improve quality. Better quality than 2 | [Docs](https://docs.freepik.com/api-reference/image-to-video/kling-v2.1-master/post-kling-v2-1-master) - [Python example](video_generation/kling_v2.1_master/python/1_gen_video.py)|

|Kling v2.1 std | Negative prompt to improve quality. Better quality than 2 | [Docs](https://docs.freepik.com/api-reference/image-to-video/kling-v2.1-std/overview) - [Python example](video_generation/kling_v2.1_std/python/1_gen_video.py)|
|Kling v2.5 pro | Negative prompt to improve quality. Better quality than 2 | [Docs](https://docs.freepik.com/api-reference/image-to-video/kling-v2.1-pro/overview) - [Python example](video_generation/kling_v2.5_pro/python/1_gen_video.py)|

|Pixverse v5 | Can generate different resolutions. Can apply some predefinied styles. Negative prompt to improve quality.| [Docs](https://docs.freepik.com/api-reference/image-to-video/pixverse/overview) - [Python example](video_generation/pixverse_v5/python/1_gen_video.py)|

|Seedance lite | Can control de aspect ratio. Can fix the camera during the video. There are 3 different models for each resolution 480p, 720p and 1080p. | 480p: [Docs](https://docs.freepik.com/api-reference/image-to-video/seedance-lite-480p/post-seedance-lite-480p) - [Python example](video_generation/seedance_lite_480p/python/1_gen_video.py) 720p: [Docs](https://docs.freepik.com/api-reference/image-to-video/seedance-lite-720p/post-seedance-lite-720p) - [Python example](video_generation/seedance_lite_720p/python/1_gen_video.py) 1080p: [Docs](https://docs.freepik.com/api-reference/image-to-video/seedance-lite-1080p/post-seedance-lite-1080p) - [Python example](video_generation/seedance_lite_1080p/python/1_gen_video.py)|

|Seedance pro | Can control de aspect ratio. Can fix the camera during the video. There are 3 different models for each resolution 480p, 720p and 1080p. Best quality than lite.| 480p: [Docs](https://docs.freepik.com/api-reference/image-to-video/seedance-pro-480p/post-seedance-pro-480p) - [Python example](video_generation/seedance_pro_480p/python/1_gen_video.py) 720p: [Docs](https://docs.freepik.com/api-reference/image-to-video/seedance-pro-720p/post-seedance-pro-720p) - [Python example](video_generation/seedance_pro_720p/python/1_gen_video.py) 1080p: [Docs](https://docs.freepik.com/api-reference/image-to-video/seedance-pro-1080p/post-seedance-pro-1080p) - [Python example](video_generation/seedance_pro_1080p/python/1_gen_video.py)|

|Wan v2.2 | Can control de aspect ratio. There are 3 different models for each resolution 480p, 580p and 720p. | 480p: [Docs](https://docs.freepik.com/api-reference/image-to-video/wan-v2-2-480p/post-wan-v2-2-480p) - [Python example](video_generation/wan_v2.2_480p/python/1_gen_video.py) 580p: [Docs](https://docs.freepik.com/api-reference/image-to-video/wan-v2-2-580p/post-wan-v2-2-580p) - [Python example](video_generation/wan_v2.2_580p/python/1_gen_video.py) 720p: [Docs](https://docs.freepik.com/api-reference/image-to-video/wan-v2-2-720p/post-wan-v2-2-720p) - [Python example](video_generation/wan_v2.2_720p/python/1_gen_video.py)|

__Many images with objects to conditioning__

| Tool | Important differences | Links|
|------|------------------------|------|
|Kling v1.6 pro elements | Can use multiple elements on different images to condion the generation. Negative prompt to improve quality. Can control the aspect ratio. | [Docs]() - [Python example](video_generation/kling_v1.6_pro_elements/python/1_gen_video.py) |
|Kling v1.6 std elements | Can use multiple elements on different images to condion the generation. Negative prompt to improve quality. Can control the aspect ratio. Worse quality than pro. | [Docs]() - [Python example](video_generation/kling_v1.6_pro_elements/python/1_gen_video.py) |

</details>

<details>
<summary><b>Text to video generation tools</b></summary>

All of them are asynchronous.

| Tool | Important differences | Links|
|------|------------------------|------|
|Minimax Hailuo 02 768p| It has automatic prompt optimizer. Resolution 768p. |[Docs]() - [Python example](video_generation/minimax_hailuo_02_768p/text_to_video/python/1_gen_video.py)|
|Minimax Hailuo 02 1080p| It has automatic prompt optimizer. Resolution 1080p.|[Docs]() - [Python example](video_generation/minimax_hailuo_02_1080p/image_to_video/python/1_gen_video.py)|

</details>

## Icon tools

### Stock resources

<details>
<summary><b>Search resources tools</b></summary>

| Tool | Description | Links|
|------|-------------|------|
| Icons | Search for icons | [Docs](https://docs.freepik.com/api-reference/icons/get-all-icons-by-order) - [Python examples](stock/1_search/icons/python) - [Curl examples](stock/1_search/icons/curl)|
</details>

<details>
<summary><b>Download resources tools</b></summary>

| Tool | Description | Links|
|------|-------------|------|
| Download icon | Download an icon by its id | [Docs](https://docs.freepik.com/api-reference/icons/download-icon-by-id) - [Python examples](stock/2_download/icons/python) - [Curl examples](stock/2_download/icons/curl)|
</details>


## MCP

Alternatively, you can use the Freepik MCP to use some of the tools directly from the Claude or Cursor chat. You can follow [the Freepik MCP documentation](https://docs.freepik.com/modelcontextprotocol) to install the MCP depending on the IDE you are using.

As an additional notes:
- You need to set up the API key in the MCP as well.
- It is necessary to have [node.js](https://nodejs.org/en/download/) installed in your machine to use the MCP.

Tools available in the MCP:

- create_video_kling_2_1_std    
- create_video_kling_2_1_pro
- get_kling_2_1_task_status     
- create_image_mystic
- get_mystic_task_status        
- detect_ai_image
- search_resources             
- get_resource_detail_by_id
- download_resource_by_id       
- get_resource_download_formats
- search_icons                  
- get_icon_detail_by_id
- download_icon_by_id