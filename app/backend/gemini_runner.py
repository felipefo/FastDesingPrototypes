import base64
import time
from typing import Awaitable, Callable, Dict
from google.genai import Client 
from google.genai import types


class Llm:
    GEMINI_2_5_FLASH_PREVIEW_05_20 = "models/gemini-2.5-flash-preview-04-17"


Completion = Dict[str, str]


async def stream_gemini_response_from_file(
    image_path: str,
    api_key: str,
    output_file: str,
    model_name: str,
) -> Completion:
    start_time = time.time()

    base_prompt = "Generate a self-contained HTML file, including inline CSS, from the provided image:"
    with open(image_path, "rb") as img_file:
        image_bytes = img_file.read()

    # Detectar MIME type
    if image_path.endswith(".png"):
        mime_type = "image/png"
    elif image_path.endswith(".jpg") or image_path.endswith(".jpeg"):
        mime_type = "image/jpeg"
    else:
        raise ValueError("Formato de imagem não suportado")

    client = Client(api_key=api_key)
    full_response = ""

    if model_name == Llm.GEMINI_2_5_FLASH_PREVIEW_05_20:
        config = types.GenerateContentConfig(
            temperature=0,
            max_output_tokens=20000,
            thinking_config=types.ThinkingConfig(
                thinking_budget=5000, include_thoughts=False
            ),
        )
    else:
        config = types.GenerateContentConfig(
            temperature=0,
            max_output_tokens=8000,
        )

    async for chunk in await client.aio.models.generate_content_stream(
        model=model_name,
        contents={
            "parts": [
                {"text": base_prompt},
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type,
                ),
            ]
        },
        config=config,
    ):
        if chunk.candidates and len(chunk.candidates) > 0:
            for part in chunk.candidates[0].content.parts:
                if not part.text:
                    continue
                full_response += part.text

    completion_time = time.time() - start_time

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_response)

    print(f"✅ HTML salvo em: {output_file}")
    return {"duration": str(completion_time), "code": full_response}
