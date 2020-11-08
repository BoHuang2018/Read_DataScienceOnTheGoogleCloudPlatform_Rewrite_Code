#!/bin/bash
source cloud_sql_configuration.sh
bash authorize_cloudshell_by_patching_authorized_networkds.sh
MYSQLIP=$(gcloud sql instances describe flights | grep ipAddress | tr ' ' '\n' | tail -1)
cat contingengcy_table_with_departure_delay_minutes.sql | sed 's/DEP_DELAY_THRESH/15/g' | sed 's/ARR_DELAY_THRESH/15/g' |
mysql --host=$MYSQLIP --user=root --password=${root_password_of_instance} --verbose

