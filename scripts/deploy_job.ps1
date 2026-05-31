# Script para desplegar la Ingesta como un Cloud Run Job

$PROJECT_ID = "esoteric-code-489918-v1" # Cambia esto por el ID de tu proyecto en GCP si es distinto
$REGION = "europe-west1"
$IMAGE_NAME = "gcr.io/$PROJECT_ID/cosora-ingest"
$JOB_NAME = "cosora-ingest-job"

Write-Host "🚀 Paso 1: Construyendo la imagen de Ingesta..." -ForegroundColor Cyan
gcloud builds submit --config cloudbuild-job.yaml

Write-Host "☁️ Paso 2: Creando/Actualizando el Cloud Run Job..." -ForegroundColor Cyan
gcloud run jobs update $JOB_NAME `
    --image $IMAGE_NAME `
    --region $REGION `
    --cpu 4 `
    --memory 8Gi `
    --max-retries 1 `
    --task-timeout 10m `
    --set-env-vars="GCP_BUCKET_NAME=rag-actas-db-bucket,DRIVE_FOLDER_ID=1cNXRxjFmUQraEIEhvZPQ00-1EvqJ_O_D"

Write-Host "✅ Job desplegado correctamente. Para lanzar la ingesta manualmente, ejecuta:" -ForegroundColor Green
Write-Host "gcloud run jobs execute $JOB_NAME --region $REGION --wait" -ForegroundColor Yellow
