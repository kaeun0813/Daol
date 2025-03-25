#!/bin/bash

echo "🚀 Cloud Function 배포 중..."
#!/bin/bash
gcloud functions deploy process_pdf_trigger \
    --runtime python310 \
    --trigger-event google.storage.object.finalize \
    --trigger-resource your-gcs-bucket \
    --region asia-northeast3 \
    --memory 512MB \
    --timeout 120s

echo "✅ 배포 완료!"
