#!/bin/bash

source gcp_configuration.sh
URL="https://${REGION}-${PROJECT}.cloudfunctions.net/${CLOUD_FUNCTION}"
echo $URL

echo {\"bucket\":\"${BUCKET}\"\,\"token\":\"${TOKEN_RUN_CLOUD_FUNCTION}\"} > /tmp/message
cat /tmp/message

curl -X POST $URL -H "Content-Type:application/json" --data-binary @/tmp/message