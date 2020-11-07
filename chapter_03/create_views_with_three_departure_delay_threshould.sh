#!/bin/bash
source cloud_sql_configuration.sh
# To run mysqlimport and mysql, authorize CloudShell
bash authorize_cloudshell_by_patching_authorized_networkds.sh

# Connect to MySQL using its IP address and do the import
MYSQLIP=$(gcloud sql instances describe flights --format="value(ipAddresses.ipAddress)")
mysql --host=$MYSQLIP --user=root --password=${root_password_of_instance} --verbose < create_views_with_three_departure_delay_threshould.sql
