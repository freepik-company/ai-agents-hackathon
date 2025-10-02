# Freepik API

Hi!

We've created this repo with a lot of examples of how to use the different tools available in the Freepik API. As there are many different tools it could be hard to find the one you need, so in this README you'll find a summary of the tools available organized by use case and and highlighting how different each of the tools is.

## Usage




## Image

### Stock resources

Freepik offers a wide range of stock resources, including images, icons and templates. Using the API you can search for resources and download them.

<details>
<summary><b>Search resources tools</b></summary>

| Tool | Description | Links|
|------|-------------|------|
| Images and templates | Search for images and templates | [Docs](https://docs.freepik.com/api-reference/resources/get-all-resources) - [Python examples](stock/1_search/images_and_templates/python) - [Curl examples](stock/1_search/images_and_templates/curl)|
| Icons | Search for icons | [Docs](https://docs.freepik.com/api-reference/icons/get-all-icons-by-order) - [Python examples](stock/1_search/icons/python) - [Curl examples](stock/1_search/icons/curl)|
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

## Video

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
<summary><b>Video generation tools</b></summary>

| Tool | Description | Important differences | Links|
|------|-------------|------------------------|------|


PREGUNTAS: 
- API search VIDEO?


# Useful documentation

[Freepik API official documentation](https://docs.freepik.com/introduction)
[Freepik API MCP](https://docs.freepik.com/modelcontextprotocol)

## Configuración de la API Key

Define la variable de entorno `FREEPIK_API_KEY` o usa el archivo `.secrets` en la raíz del proyecto (ignorados por git).

### Opción A: Variable de entorno (recomendada)

En macOS con zsh:

```bash
export FREEPIK_API_KEY="tu_api_key_aqui"
```

Para que persista en nuevas terminales, añade la línea anterior a tu `~/.zshrc` y recarga:

```bash
echo 'export FREEPIK_API_KEY="tu_api_key_aqui"' >> ~/.zshrc && source ~/.zshrc
```

### Opción B: Archivo `.secrets`

Crea un archivo `.secrets` en la raíz del repo con solo la API key en una línea:

```text
TU_API_KEY
```

El módulo `python/freepik_api.py` leerá primero la variable de entorno y, si no existe, intentará usar `.secrets`.


# Curl examples

Step 1: Export the API key

```bash
export FREEPIK_API_KEY="your_api_key"
```

Step 2: Run the curl command

```bash


DUDAS:
 - En la API de iconos veo la url del thumbnail pero no veo la url del icono en sí. ¿Cómo puedo obtener la url del icono?
 - 


kling funciona igual las versiones:
 - 1.6 pro - admite frame inicial y final
    - check: "https://api.freepik.com/v1/ai/image-to-video/kling/{task-id}"
 - 1.6 std - admite frame inicial. Los params igual que 1.6-std pero sin image_tail
    - check: "https://api.freepik.com/v1/ai/image-to-video/kling/{task-id}"
 - 2 - admite frame inicial. Los params igual que 1.6-std pero sin image_tail
    - check: "https://api.freepik.com/v1/ai/image-to-video/kling-v2/{task-id}"
 - 2.1 std - admite frame inicial. Los params igual que 1.6-std pero sin image_tail
    - check:  "https://api.freepik.com/v1/ai/image-to-video/kling-v2-1/{task-id}"
 - 2.1 pro - admite frame inicial y final. Los params igual que 1.6-std
    - check :  "https://api.freepik.com/v1/ai/image-to-video/kling-v2-1/{task-id}"
 - 2.1 master - admite frame inicial. Los params igual que 1.6-std pero sin image_tail
    - check: "https://api.freepik.com/v1/ai/image-to-video/kling-v2-1-master/{task-id}"
 - 2.5 pro - admite frame inicial. Los params igual que 1.6-std pero sin image_tail.
    - Check: "https://api.freepik.com/v1/ai/image-to-video/kling-v2-5-pro/{task-id}"
- 1.6 elements: Igual que los otros pero con varias imagenes para pasarle.

- minimax: Tienen dos tareas, text_to_video o image_to_video. Tienen los mismos params los dos. frame inicial y final.
- seedance: Todos iguales, frame inicial y cambia aspect ratio.
- Wan: Todos iguales, frame inicial y cambia aspect ratio.
- PixVerse: Todos meten estilo
    - PixVerse-v5: Frame inicial.
    - PixVerse-v5-transition: Frame inicial y final.

MAGNIFIC PRECISION: No devuelven el image_url despues de hacer el upscale.



# MCP

Instalacion: necesita node

Tools disponibles en el MCP:
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


















### Stock resources

Freepik offers a wide range of stock video. Using the API you can search for resources and download them.

<details>
<summary><b>Search resources tools</b></summary>

| Tool | Description | Links|
|------|-------------|------|
| Images and templates | Search for images and templates | [Docs](https://docs.freepik.com/api-reference/resources/get-all-resources) - [Python examples](stock/1_search/images_and_templates/python) - [Curl examples](stock/1_search/images_and_templates/curl)|
| Icons | Search for icons | [Docs](https://docs.freepik.com/api-reference/icons/get-all-icons-by-order) - [Python examples](stock/1_search/icons/python) - [Curl examples](stock/1_search/icons/curl)|
| Videos | Search for videos | [Docs](https://docs.freepik.com/api-reference/videos/get-all-videos-by-order) - [Python examples](stock/1_search/videos/python) - [Curl examples](stock/1_search/videos/curl)|
</details>
  
    
<details>
<summary><b>Download resources tools</b></summary>

| Tool | Description | Links|
|------|-------------|------|
| Download image and template | Download an image or a template by its id | [Docs](https://docs.freepik.com/api-reference/resources/download-a-resource) - [Python examples](stock/2_download/images_and_templates/python) - [Curl examples](stock/2_download/images_and_templates/curl)|
| Download icon | Download an icon by its id | [Docs](https://docs.freepik.com/api-reference/icons/download-icon-by-id) - [Python examples](stock/2_download/icons/python) - [Curl examples](stock/2_download/icons/curl)|
| Download video | Download a video by its id | [Docs](https://docs.freepik.com/api-reference/videos/download-video-by-id) - [Python examples](stock/2_download/videos/python) - [Curl examples](stock/2_download/videos/curl)|

</details>
