#!/usr/bin/env python

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil
import logging
import os.path
import zipfile
import datetime
import tempfile
import ssl
from google.cloud import storage
from google.cloud.storage import Blob
from urllib.request import urlopen as impl
from params_of_downloading import params_to_form_downloaded_data as request_params
from params_of_downloading import expected_header

ctx_no_secure = ssl.create_default_context()
ctx_no_secure.set_ciphers('HIGH:!DH:!aNULL')
ctx_no_secure.check_hostname = False
ctx_no_secure.verify_mode = ssl.CERT_NONE

path_of_bucket_store_csv = 'flights/raw/'


class DataUnavailable(Exception):
    def __init__(self, message):
        self.message = message


class UnexpectedFormat(Exception):
    def __init__(self, message):
        self.message = message


class FlightRecordsDownloader:
    def __init__(self, year_of_flights, month_of_flights, destination_directory_to_store_downloaded):
        self.request_url_to_download_flights_record_from_bts = \
            'https://www.transtats.bts.gov/DownLoad_Table.asp?Table_ID=236&Has_Group=3&Is_Zipped=0'
        self.params_to_form_downloaded_data = request_params.format(year_of_flights, month_of_flights)
        self.downloaded_zipfile_name_with_path = \
            os.path.join(destination_directory_to_store_downloaded,
                         "{}{}.zip".format(year_of_flights, month_of_flights))
        self.download_data_from_bts_as_zip()
        self.csv_file_with_flights_record_extracted_from_downloaded_zip_file = \
            self.convert_downloaded_zip_to_csv(self.downloaded_zipfile_name_with_path,
                                               destination_directory_to_store_downloaded)

    def send_request_get_response_with_data(self):
        return impl(self.request_url_to_download_flights_record_from_bts,
                    self.params_to_form_downloaded_data.encode('utf-8'),
                    context=ctx_no_secure)

    def download_data_from_bts_as_zip(self):
        with open(self.downloaded_zipfile_name_with_path, "wb") as zip_file:
            response_with_data = self.send_request_get_response_with_data()
            zip_file.write(response_with_data.read())
        return

    def convert_downloaded_zip_to_csv(self, downloaded_zip_file, destination_directory_for_csv_file):
        zip_file_reading = zipfile.ZipFile(downloaded_zip_file, 'r')
        self.extract_all_members_from_archive_zip_to_destination_directory(zip_file_reading,
                                                                           destination_directory_for_csv_file)
        csv_file_flights_record = \
            self.generate_csv_file_with_members_extracted_from_zip_file(zip_file_reading,
                                                                        destination_directory_for_csv_file)
        zip_file_reading.close()
        return csv_file_flights_record

    @staticmethod
    def extract_all_members_from_archive_zip_to_destination_directory(zip_file_read_object, destination_directory_path):
        current_working_directory = os.getcwd()
        os.chdir(destination_directory_path)
        zip_file_read_object.extractall()
        os.chdir(current_working_directory)
        return

    @staticmethod
    def generate_csv_file_with_members_extracted_from_zip_file(zip_file_read_object_extracted,
                                                               destination_directory_path):
        return os.path.join(destination_directory_path, zip_file_read_object_extracted.namelist()[0])


class DataVerificationRemoveUnqualifiedCsvFile:
    def __init__(self, csv_file_with_download_data, expected_hearders_of_csv_flights_record):
        with open(csv_file_with_download_data, 'r') as downloaded_csv_file_read:
            first_line_of_csv = downloaded_csv_file_read.readline().strip()
            if not self.csv_file_has_expected_headers(first_line_of_csv, expected_hearders_of_csv_flights_record):
                os.remove(csv_file_with_download_data)
                logging.error("Got header={} \n expected_header={}".format(first_line_of_csv,
                                                                           expected_hearders_of_csv_flights_record))
                raise UnexpectedFormat("Headers of csv are not same as expected headers")
            second_line_of_csv = next(downloaded_csv_file_read, None)
            if not self.csv_file_has_content_data(second_line_of_csv):
                os.remove(csv_file_with_download_data)
                raise DataUnavailable("Received a file from BTS that has only the header and no content")

    @staticmethod
    def csv_file_has_expected_headers(first_line_read_of_csv, expected_header_in_string):
        if first_line_read_of_csv != expected_header_in_string:
            return False
        else:
            return True

    @staticmethod
    def csv_file_has_content_data(second_line_read_of_csv):
        if isinstance(second_line_read_of_csv, type(None)):
            return False
        else:
            return True


class DataCleanAfterDownload:
    def __init__(self, csv_after_verification, year_of_csv, month_of_csv):
        self.csv_after_verification = csv_after_verification
        self.year_of_csv = year_of_csv
        self.month_of_csv = month_of_csv
        self.csv_with_cleaned_data = self.implement_data_clean_remove_uncleaned_csv()

    def implement_data_clean_remove_uncleaned_csv(self):
        csv_for_clean_data = self.generate_csv_for_cleaned_data_in_directory_of_uncleaned_csv()
        with open(self.csv_after_verification, 'r') as uncleaned_csv:
            with open(csv_for_clean_data, 'w') as clean_csv:
                for line in uncleaned_csv:
                    line_without_trailing_comma = self.remove_trailing_comma_from_line_in_csv(line)
                    line_without_quote_trailing_comma = self.remove_quote_from_line_in_csv(line_without_trailing_comma)
                    clean_csv.write(line_without_quote_trailing_comma)
                    clean_csv.write('\n')
        os.remove(self.csv_after_verification)
        return csv_for_clean_data

    def generate_csv_for_cleaned_data_in_directory_of_uncleaned_csv(self):
        return os.path.join(os.path.dirname(self.csv_after_verification),
                            '{}{}.csv'.format(self.year_of_csv, self.month_of_csv))

    @staticmethod
    def remove_trailing_comma_from_line_in_csv(line_in_csv):
        return line_in_csv.rstrip().rstrip(',')

    @staticmethod
    def remove_quote_from_line_in_csv(line_in_csv):
        return line_in_csv.translate(str.maketrans('', '', '"'))


class UploadCleanCsvToCloudStorage:
    def __init__(self, bucket_name_in_cloud_storage, path_in_bucket, csv_cleaned):
        self.blob_name_in_bucket = path_in_bucket + os.path.basename(csv_cleaned)
        self.target_uploading_blob = self.get_target_blob_of_uploading(bucket_name_in_cloud_storage,
                                                                       self.blob_name_in_bucket)
        self.target_uploading_blob.upload_from_filename(csv_cleaned)
        self.complete_target_cloud_storage_location = 'gs://{}/{}'.format(bucket_name_in_cloud_storage,
                                                                          self.blob_name_in_bucket)

    @staticmethod
    def get_target_blob_of_uploading(target_bucket_name, target_blob_name):
        cloud_storage_client = storage.Client()
        target_bucket = cloud_storage_client.get_bucket(target_bucket_name)
        return Blob(target_blob_name, target_bucket)


class CalculateYearMonthToDownloadFromBTSbyMostRecentRecordOnCloudStorage:
    def __init__(self, bucket_name_in_cloud_storage, path_in_bucket):
        self.list_of_csv_names_stored_in_cloud_storage = \
            self.get_list_of_csv_names_stored_in_cloud_storage(bucket_name_in_cloud_storage, path_in_bucket)
        self.year_month_string_tuple_of_latest_csv_in_cloud_storage = \
            self.get_year_month_string_of_latest_csv_in_cloud_storage(self.list_of_csv_names_stored_in_cloud_storage)
        self.year_string_of_latest_csv_in_cloud_storage = self.year_month_string_tuple_of_latest_csv_in_cloud_storage[0]
        self.month_string_of_latest_csv_in_cloud_storage = self.year_month_string_tuple_of_latest_csv_in_cloud_storage[
            1]
        self.next_month_with_year_to_latest_csv_in_cloud_storage = \
            self.get_next_month_with_year_to_latest_csv_in_cloud_storage(
                self.year_string_of_latest_csv_in_cloud_storage,
                self.month_string_of_latest_csv_in_cloud_storage
            )

    @staticmethod
    def get_list_of_csv_names_stored_in_cloud_storage(target_bucket_name, path_in_bucket):
        cloud_storage_client = storage.Client()
        target_bucket_includes_blobs = cloud_storage_client.get_bucket(target_bucket_name)
        target_blobs_include_flight_records = list(target_bucket_includes_blobs.list_blobs(prefix=path_in_bucket))
        return [blob.name for blob in target_blobs_include_flight_records if 'csv' in blob.name]

    @staticmethod
    def get_year_month_string_of_latest_csv_in_cloud_storage(list_of_csv_file_names):
        if not list_of_csv_file_names:
            return "No flight records on Cloud Storage"
        latest_csv_file_name = os.path.basename(list_of_csv_file_names[-1])
        year_of_csv_string = latest_csv_file_name[:4]
        month_of_csv_string = latest_csv_file_name[4:6]
        return year_of_csv_string, month_of_csv_string

    @staticmethod
    def get_next_month_with_year_to_latest_csv_in_cloud_storage(year_of_latest_csv_string, month_of_latest_csv_string):
        date_of_latest_csv = datetime.datetime(int(year_of_latest_csv_string), int(month_of_latest_csv_string), 15)
        date_of_next_month = date_of_latest_csv + datetime.timedelta(30)
        return '{}'.format(date_of_next_month.year), '{:02d}'.format(date_of_next_month.month)


def download_bts_flights_records_upload_cloud_storage(upload_bucket_in_cloud_storage, path_in_bucket,
                                                      year_of_flights_string_four_digits=None,
                                                      month_of_flights_string_two_digits=None):
    if isinstance(year_of_flights_string_four_digits, type(None)) or \
            isinstance(month_of_flights_string_two_digits, type(None)):
        download_month_year_calculation = \
            CalculateYearMonthToDownloadFromBTSbyMostRecentRecordOnCloudStorage(upload_bucket_in_cloud_storage,
                                                                                path_in_bucket)
        year_month_strings_tuple_download = \
            download_month_year_calculation.next_month_with_year_to_latest_csv_in_cloud_storage
        year_of_flights = year_month_strings_tuple_download[0]
        month_of_flights = year_month_strings_tuple_download[1]
    else:
        year_of_flights = year_of_flights_string_four_digits
        month_of_flights = month_of_flights_string_two_digits
    try:
        implement_download_clean_verify_upload(year_of_flights, month_of_flights,
                                               upload_bucket_in_cloud_storage, path_in_bucket)
    except DataUnavailable as e:
        logging.info('Try again later: {}'.format(e.message))
    return


def implement_download_clean_verify_upload(year_of_flights, month_of_flights, upload_bucket_in_cloud_storage,
                                           path_in_bucket):
    temporary_directory_store_downloaded_data = tempfile.mkdtemp(prefix='ingest_flights')
    download_flights_record_csv = FlightRecordsDownloader(year_of_flights, month_of_flights,
                                                          temporary_directory_store_downloaded_data)
    downloaded_csv = download_flights_record_csv.csv_file_with_flights_record_extracted_from_downloaded_zip_file
    clean_downloaded_data_csv = DataCleanAfterDownload(downloaded_csv, year_of_flights, month_of_flights)
    cleaned_data_csv = clean_downloaded_data_csv.csv_with_cleaned_data
    DataVerificationRemoveUnqualifiedCsvFile(cleaned_data_csv, expected_header)
    upload_cleaned_data_csv = UploadCleanCsvToCloudStorage(upload_bucket_in_cloud_storage, path_in_bucket,
                                                           cleaned_data_csv)
    logging.info('Uploaded flight-records in csv of {}-{} to {}'
                 .format(year_of_flights, month_of_flights,
                         upload_cleaned_data_csv.complete_target_cloud_storage_location))
    shutil.rmtree(temporary_directory_store_downloaded_data)
    return


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='ingest flights data from BTS website to Google Cloud Storage')
    parser.add_argument('--bucket', help='GCS bucket to upload data to', required=True)
    parser.add_argument('--year', help='Example: 2015.  If not provided, defaults to getting next month')
    parser.add_argument('--month', help='Specify 01 for January. If not provided, defaults to getting next month')

    try:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
        args = parser.parse_args()
        download_bts_flights_records_upload_cloud_storage(
            upload_bucket_in_cloud_storage=args.bucket,
            path_in_bucket=path_of_bucket_store_csv,
            year_of_flights_string_four_digits=args.year,
            month_of_flights_string_two_digits=args.month
        )
    except DataUnavailable as e:
        logging.info('Try again later: {}'.format(e.message))
