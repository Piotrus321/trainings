import logging
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import pandas as pd
import azure.functions as func
import os
import openpyxl
from io import BytesIO
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function has recieved the request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        try:
            default_credential = DefaultAzureCredential(exclude_shared_token_cache_credential=True)
            mappings = json.loads(os.environ["mappings"])
            blob_service_client = BlobServiceClient(
                account_url = os.environ["azureBlobStorageEndpoint"],
                credential = default_credential
            )
            container_client = blob_service_client.get_container_client(
                container = 'fa-test-container'
            )
            raw_data = container_client.download_blob(f"staging/{name}").readall()
            wb = openpyxl.load_workbook(filename=BytesIO(raw_data), read_only=True)
            sheet_obj = wb['Production']
            cell_dict = {}
            for k,v in mappings["cell_mappings"].items():
                cell_dict.update({k:sheet_obj[v].value})
            report_date = cell_dict['Report_date']
            factory = cell_dict['Factory']
            df = pd.read_excel(raw_data, skiprows=mappings["dataframe_mappings"]["SkipRows"])
            df = pd.melt(df, id_vars=df.columns[0], var_name='Brand',value_name='Production')
            df.insert(1,'ReportDate', report_date)
            df.insert(2,'Factory',factory)
            container_client.upload_blob(
                name = f"extracted-Http/production_report_{factory}_{report_date.date()}.csv",
                data = pd.DataFrame.to_csv(df, index=False),
                overwrite = True
            )
            container_client.delete_blob(
                name = f"staging-http/{name}"
            )
        except Exception as e:
            return func.HttpResponse(str(e))

        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.", status_code=500)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
