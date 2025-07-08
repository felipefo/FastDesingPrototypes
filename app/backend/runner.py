import asyncio
from gemini_runner import stream_gemini_response_from_file, Llm

async def main():
    await stream_gemini_response_from_file(
        image_path="exemplo.png",             # Caminho da imagem local
        output_file="index.html",             # Arquivo onde o HTML será salvo
        api_key="",                # 🔑 Substitua pela sua chave Gemini
        model_name=Llm.GEMINI_2_5_FLASH_PREVIEW_05_20
    )

if __name__ == "__main__":
    asyncio.run(main())
