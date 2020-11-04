#!/bin/bash
source cloud_sql_configuration.sh
gcloud sql instances create ${name_of_instance} \
    --tier=${tier_of_cloud_sql} --activation-policy=${activation_policy_of_sql} --zone=${compute_engine_zone}

echo "Please go to the GCP console and change the root password of the instance"
