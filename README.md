

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
