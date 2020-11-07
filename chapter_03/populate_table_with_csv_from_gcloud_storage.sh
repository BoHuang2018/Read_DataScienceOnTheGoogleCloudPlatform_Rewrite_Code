#!/bin/bash
source cloud_sql_configuration.sh
source cloud_storage_configuration.sh

echo "Populating Cloud SQL instance flights from gs://${bucket_in_cloud_storage}/${directory_of_csv_in_bucket}/..."

bash authorize_cloudshell_by_patching_authorized_networkds.sh

# the table name for mysqlimport comes from the filename, so rename our CSV files, changing bucket name as needed
counter_in_loop=0
#for FILE in $(gsutil ls gs://${BUCKET}/flights/raw/2015*.csv); do
#   gsutil cp $FILE flights.csv-${counter}
for csv_file in 201501.csv 201507.csv; do
   gsutil cp gs://${bucket_in_cloud_storage}/${directory_of_csv_in_bucket}/$csv_file flights.csv-${counter_in_loop}
   counter_in_loop=$((counter_in_loop+1))
done

# import csv files
sql_public_ip_address=$(gcloud sql instances describe ${name_of_instance} --format="value(ipAddresses.ipAddress)")
mysqlimport --local --host=$sql_public_ip_address --user=root --ignore-lines=1 --fields-terminated-by=',' --password=${root_password_of_instance} bts flights.csv-*
rm flights.csv-*