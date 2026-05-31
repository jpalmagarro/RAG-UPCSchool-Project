import os
from google.cloud import storage
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def download_folder_from_gcs(bucket_name, source_folder, destination_folder):
    """
    Descarga una carpeta completa desde un bucket de GCS a un directorio local.
    """
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=source_folder)
        
        count = 0
        for blob in blobs:
            if blob.name.endswith("/"):
                continue  # Skip directorios vacios
            
            # Crear ruta local
            relative_path = os.path.relpath(blob.name, source_folder)
            local_path = os.path.join(destination_folder, relative_path)
            
            # Asegurar que los subdirectorios existan
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Descargar archivo
            blob.download_to_filename(local_path)
            count += 1
            
        logging.info(f"✅ Descarga completada: {count} archivos descargados a {destination_folder}.")
    except Exception as e:
        logging.error(f"❌ Error descargando la base de datos de GCS: {e}")
        logging.error("Asegúrate de que estás autenticado con 'gcloud auth application-default login'")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")
    if not BUCKET_NAME:
        logging.error("La variable GCP_BUCKET_NAME no está configurada en el archivo .env")
        exit(1)
        
    DESTINATION = "./data/chroma_db"
    
    logging.info(f"Iniciando descarga de ChromaDB desde gs://{BUCKET_NAME}/chroma_db ...")
    download_folder_from_gcs(BUCKET_NAME, "chroma_db", DESTINATION)
