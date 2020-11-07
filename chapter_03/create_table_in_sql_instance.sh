#!/bin/bash
source cloud_sql_configuration.sh

bash authorize_cloudshell_by_patching_authorized_networkds.sh

# Connect to MySQL using its IP address and do the import
sql_public_ip_address=$(gcloud sql instances describe ${name_of_instance} --format="value(ipAddresses.ipAddress)")
mysql --host=$sql_public_ip_address --user=root --password=${root_password_of_instance} --verbose < create_table.sql
