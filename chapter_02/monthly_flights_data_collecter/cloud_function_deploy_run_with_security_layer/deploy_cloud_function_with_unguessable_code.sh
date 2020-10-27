URL=flights_data_collect$(openssl rand -base64 38 | tr -d /=+ | cut -c -32)
echo $URL

gcloud functions deploy $URL --entry-point flights_data_collect --runtime python38 --trigger-http --timeout 480s --memory=1024MB --allow-unauthenticated