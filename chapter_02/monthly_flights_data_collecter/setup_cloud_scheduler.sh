#!/bin/bash
source gcp_configuration.sh

URL="https://${REGION}-${PROJECT}.cloudfunctions.net/${CLOUD_FUNCTION}"
echo {\"bucket\":\"${BUCKET}\", \"token\":\"${TOKEN_RUN_CLOUD_FUNCTION}\"} > /tmp/message.json

cat /tmp/message.json
gcloud scheduler jobs create http flights_data_collect \
       --schedule="27 of month 08:05" \
       --uri=$URL \
       --max-backoff=7d \
       --max-retry-attempts=5 \
       --max-retry-duration=3h \
       --min-backoff=1h \
       --time-zone="America/New_York" \
       --message-body-from-file=/tmp/message.json
