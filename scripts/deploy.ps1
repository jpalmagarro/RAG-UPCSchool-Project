# === SCRIPT DE DESPLIEGUE A GOOGLE CLOUD RUN ===

# 1. Configura tu ID de proyecto de Google Cloud (Reemplaza 'TU-PROYECTO-ID' por el ID real de tu proyecto GCP)
$PROJECT_ID = "esoteric-code-489918-v1"
$REGION = "europe-west1"
$IMAGE_NAME = "gcr.io/$PROJECT_ID/cosora-demo"

Write-Host "Iniciando proceso de construcción automatizado en Google Cloud Build..." -ForegroundColor Cyan
# 2. Compilar usando Cloud Build (Esto lee cloudbuild.yaml, descarga la base de datos del bucket y luego compila Docker)
gcloud builds submit --config cloudbuild.yaml

Write-Host "Construcción finalizada. Iniciando despliegue en Cloud Run..." -ForegroundColor Cyan
# 3. Desplegar la imagen en Cloud Run
gcloud run deploy cosora-demo `
    --image $IMAGE_NAME `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --memory 8Gi `
    --cpu 4

Write-Host "¡Despliegue finalizado!" -ForegroundColor Green
Write-Host "Recuerda ir a la consola de Google Cloud Run -> Servicio 'cosora-demo' -> Editar -> Variables" -ForegroundColor Yellow
Write-Host "Y añadir tu variable OPENAI_API_KEY allí de forma segura." -ForegroundColor Yellow
