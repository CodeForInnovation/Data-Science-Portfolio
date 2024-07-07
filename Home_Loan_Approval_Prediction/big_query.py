from google.cloud import bigquery
from google.oauth2 import service_account
import os
import base64
import json

class BigQuery:
    def __init__(self):
        encoded_credentials = os.getenv('BIGQUERY_KEY')

        # Decode the base64-encoded credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')

        # Set Google Application Credentials

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = decoded_credentials

        self.dataset = 'home_loan'
        self.table = 'home_loan_approval'
        credentials_dict = json.loads(decoded_credentials)

        self.credentials = service_account.Credentials.from_service_account_info(credentials_dict)

        # Initialize BigQuery client with the credentials
        self.client = bigquery.Client(credentials=self.credentials, project=self.credentials.project_id)
        self.table_ref = self.client.dataset(self.dataset).table(self.table)

    def load_data(self,data):
        job = self.client.load_table_from_dataframe(data, self.table_ref)
        result = job.result()
        return result
        