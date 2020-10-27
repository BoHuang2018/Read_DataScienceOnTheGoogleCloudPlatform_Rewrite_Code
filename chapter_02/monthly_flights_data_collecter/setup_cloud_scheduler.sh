#!/bin/bash
source gcp_configuration.sh

URL="https://${REGION}-${PROJECT}.cloudfunctions.net/${CLOUD_FUNCTION}"
echo {\"bucket\":\"${BUCKET}\", \"token\":\"${TOKEN_RUN_CLOUD_FUNCTION}\"} > /tmp/message.json

gcloud pubsub topics create cron-topic-flights_data_collect
gcloud pubsub subscriptions create cron-sub-flights_data_collect --topic cron-topic-flights_data_collect
cat /tmp/message.json
gcloud scheduler jobs create http flights_data_collect \
       --schedule="27 of month 08:05" \
       --uri=$URL \
       --max-backoff=7d \
       --max-retry-attempts=5 \
       --max-retry-duration=3h \
       --min-backoff=1h \
       --time-zone="US/Eastern" \
       --message-body-from-file=/tmp/message.json
