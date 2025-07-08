import re
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from update_flow import EstadoInputPrototipoUpdate, update_prototipo
from gemini_runner import stream_gemini_response_from_file, Llm
import os
import shutil
import uuid
from fastapi.responses import JSONResponse


from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
app = FastAPI()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))



@app.get("/", response_class=FileResponse)
async def root():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="index.html não encontrado.")
    return FileResponse(index_path)


@app.post("/gerar_html")
async def gerar_html(imagem: UploadFile = File(...)):
    if not imagem.filename.endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="Formato de imagem não suportado.")

    try:
        ext = os.path.splitext(imagem.filename)[-1]
        unique_filename = f"{uuid.uuid4().hex}{ext}"
        temp_path = os.path.join(UPLOAD_DIR, unique_filename)

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(imagem.file, buffer)

        output_filename = unique_filename.replace(ext, ".html")
        output_path = os.path.join(UPLOAD_DIR, output_filename)

        await stream_gemini_response_from_file(
            image_path=temp_path,
            output_file=output_path,
            api_key=API_KEY,
            model_name=Llm.GEMINI_2_5_FLASH_PREVIEW_05_20,
        )

        with open(output_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        html_content = limpar_html_bruto(html_content)

        return JSONResponse(
            content={
                "code": html_content,
                "filename": output_filename
            },
            status_code=200
        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


def limpar_html_bruto(texto: str) -> str:
    # Remove blocos que começam com ```html, ```css, ```script e terminam com ```
    texto = re.sub(r"```(html|css|script)?\n?", "", texto, flags=re.IGNORECASE)
    texto = texto.replace("```", "")  # Remove fechamento
    return texto.strip()


@app.post("/aplicar_ajuste")
async def gerar_ajustes(data: EstadoInputPrototipoUpdate):
    try:
        # Gere HTML ajustado (exemplo: aqui você chama seu agente)
        resultado = await update_prototipo(data)
        resultado_html = resultado.get("codigo")
        # Limpa o HTML, se necessário
        resultado_html = limpar_html_bruto(resultado_html)

        # Cria nome único para o arquivo ajustado
        unique_filename = f"{uuid.uuid4().hex}.html"
        output_path = os.path.join(UPLOAD_DIR, unique_filename)

        # Salva o HTML ajustado no mesmo diretório
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(resultado_html)

        # Retorna igual ao gerar_html
        return JSONResponse(
            content={
                "code": resultado_html,
                "filename": unique_filename
            },
            status_code=200
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


FRONTEND_DIR  = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/", StaticFiles(directory=FRONTEND_DIR   , html=True), name="static")