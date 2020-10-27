import logging
from flask import escape
from download_flights_data_ingest_CloudStorage import download_bts_flights_records_upload_cloud_storage
from download_flights_data_ingest_CloudStorage import path_of_bucket_store_csv
from download_flights_data_ingest_CloudStorage import DataUnavailable
import json


def flights_data_collect(request):
    try:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
        request_json = extract_parameters_in_json_from_request(request)
        if halt_cloud_function_when_token_unmatch(escape(request_json['token'])):
            return
        year_of_flights = escape(request_json['year']) if 'year' in request_json else None
        month_of_flights = escape(request_json['month']) if 'month' in request_json else None
        bucket_in_cloud_storage = escape(request_json['bucket'])  # required
        download_bts_flights_records_upload_cloud_storage(bucket_in_cloud_storage, path_of_bucket_store_csv,
                                                          year_of_flights, month_of_flights)
        return 'Done'
    except DataUnavailable as e:
        logging.info('Try again later: {}'.format(e.message))


def halt_cloud_function_when_token_unmatch(token):
    if token != 'BwbMjrbWr5YlYWirpwOcQk3UL2wGgyQ8':
        logging.info("Ignoring request without valid token")
        return True
    return False


def extract_parameters_in_json_from_request(request):
    request_json = request.get_json()
    if isinstance(request_json, type(None)) and request.headers.get("Content-Type") == "application/octet-stream":
        raw_request_data = request.data
        string_request_data = raw_request_data.decode("utf-8")
        request_json: dict = json.loads(string_request_data)
    return request_json