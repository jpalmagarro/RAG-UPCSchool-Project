FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirements.txt

# Pre-descargar el modelo de IA y aislarlo en una carpeta local
RUN python -c "from transformers import AutoTokenizer, AutoModel; AutoTokenizer.from_pretrained('intfloat/multilingual-e5-base').save_pretrained('./hf_model'); AutoModel.from_pretrained('intfloat/multilingual-e5-base').save_pretrained('./hf_model')"

# Copiamos la carpeta src entera
COPY src/ ./src/

# Copiamos la base de datos DESDE LOCAL (data/chroma_db). 
# En la nube (GCP), cloudbuild.yaml se encarga de descargarla aquí ANTES de lanzar Docker.
# En local, el desarrollador usa download_db.py antes de compilar.
COPY data/chroma_db ./data/chroma_db

EXPOSE 8080
HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health

ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=8080", "--server.address=0.0.0.0"]
