# COSORA Demo - RAG UPCSchool Project

## 📌 About the Project
This is a **Retrieval-Augmented Generation (RAG)** demo designed to analyze construction site meeting minutes ("actas de obra"). It allows users to ask natural language questions about construction progress and get answers backed by official documents.

This project was developed for the **UPCSchool**, demonstrating how to integrate AI into engineering and construction workflows.

## 🏗️ Architecture
The system uses a **Serverless Architecture on Google Cloud Platform (GCP)** for low cost and high scalability:

- **Frontend:** [Streamlit](https://streamlit.io/) hosted on Google Cloud Run.
- **Vector Database:** [ChromaDB](https://www.trychroma.com/).
- **AI Models:**
  - **Search (Embeddings):** `intfloat/multilingual-e5-base` running locally for fast hybrid search.
  - **Text Generation (LLM):** OpenAI API (`gpt-4o-mini`).
- **Data Pipeline (Cloud Run Job):**
  1. Downloads `.doc` and `.docx` files from Google Drive.
  2. Extracts text using `antiword` and python-docx.
  3. Chunks the text, creates embeddings, and builds the ChromaDB database.
  4. Uploads the ready-to-use database to Google Cloud Storage.

## 🚀 Deployment
We use Google Cloud Build and PowerShell scripts for CI/CD:
- **`deploy_job.ps1`**: Deploys the Data Ingestion Job.
- **`deploy.ps1`**: Deploys the Web App. The 1GB HuggingFace model is pre-downloaded and baked into the Docker image to ensure instant cold starts and prevent timeout crashes.

## 🔐 Environment Variables Required
To run this project, you need to set up the following secrets in Cloud Run:
- `OPENAI_API_KEY`: Your OpenAI API key.
- `APP_PASSWORD`: A password to protect the web UI.
- `GCP_BUCKET_NAME`: The Google Cloud Storage bucket name.
- `DRIVE_FOLDER_ID`: The Google Drive folder ID containing your source documents.
