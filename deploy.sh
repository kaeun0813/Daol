BUCKET_NAME=$(gcloud storage buckets list --format="value(name)" | grep summarize-pdf)
if [ -z "$BUCKET_NAME" ]; then
  echo "❌ PDF 버킷을 찾을 수 없습니다!"
  exit 1
fi

echo "✅ 배포할 버킷: $BUCKET_NAME"

gcloud functions deploy summarize_pdf_gcs \
  --runtime python310 \
  --trigger-event google.storage.object.finalize \
  --trigger-resource "$BUCKET_NAME" \
  --entry-point summarize_pdf_gcs \
  --env-vars-file .env.yaml
