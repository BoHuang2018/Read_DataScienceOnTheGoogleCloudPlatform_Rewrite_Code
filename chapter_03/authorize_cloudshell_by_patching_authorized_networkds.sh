#!/bin/bash
source cloud_sql_configuration.sh
gcloud sql operations list --instance=${name_of_instance} --filter='NOT status:done' --format='value(name)' | xargs -r gcloud sql operations wait
gcloud sql instances patch ${name_of_instance} \
	--authorized-networks $(wget -qO - http://ipecho.net/plain)/32
