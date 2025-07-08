FROM python:3.11-slim-bookworm

WORKDIR /app
RUN mkdir -p ./frontend
RUN mkdir -p ./output

# Copia código do backend
COPY ./backend /app

# Copia o build gerado pelo estágio anterior
COPY ./frontend/ /frontend

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "10"]
