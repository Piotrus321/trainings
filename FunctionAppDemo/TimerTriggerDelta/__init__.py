import datetime
import logging
from azure.storage.blob import BlobServiceClient
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import os
from deltalake import DeltaTable
from deltalake.writer import write_deltalake
import pandas as pd

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    
    default_credential = DefaultAzureCredential(exclude_shared_token_cache_credential=True)
    key_vault_url = os.environ["keyVaultUri"]
    secret_name = os.environ["secretName"]
    secret_client = SecretClient(vault_url=key_vault_url, credential=default_credential)
    secret_value = secret_client.get_secret(secret_name).value
    delta_table_path = f"abfss://fa-test-container@dlfademoprep01.dfs.core.windows.net/delta-test"
    storage_options = {"azure_storage_account_name": "dlfademoprep01", 
                       "azure_storage_access_key": secret_value} 
    
    blob_service_client = BlobServiceClient(account_url="https://dlfademoprep01.blob.core.windows.net/", credential=secret_value)
    container_client = blob_service_client.get_container_client('fa-test-container')
    

    for blob in container_client.list_blobs(name_starts_with='extracted-Http/'):
        raw_data = container_client.download_blob(blob.name)
        df = pd.read_csv(raw_data)
        write_deltalake(table_or_uri=delta_table_path, data=df, storage_options=storage_options, mode='append')
        container_client.delete_blob(blob=blob.name)
    delta_blobs = container_client.list_blobs(name_starts_with='delta-test/')
    delta_file_count = sum(1 for blob in delta_blobs if 'json' not in blob.name)
    if delta_file_count>10:
        dt = DeltaTable(delta_table_path,storage_options=storage_options)
        dt.optimize.compact()
        dt.vacuum(retention_hours=0, enforce_retention_duration=False, dry_run=False)

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
