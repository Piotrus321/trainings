import logging
import json
import os
import azure.functions as func
import pandas as pd
import openpyxl
from io import BytesIO


def main(myblob: func.InputStream, outputBlob: func.Out[bytes]):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    mappings = json.loads(os.environ["mappings"])
    input_blob = myblob.read()
    wb = openpyxl.load_workbook(filename=BytesIO(input_blob), read_only=True)
    sheet_obj = wb['Production']
    cell_dict = {}
    for k,v in mappings["cell_mappings"].items():
        cell_dict.update({k:sheet_obj[v].value})
    report_date = cell_dict['Report_date']
    factory = cell_dict['Factory']
    df = pd.read_excel(BytesIO(input_blob), skiprows=mappings["dataframe_mappings"]["SkipRows"])
    df = pd.melt(df, id_vars=df.columns[0], var_name='Brand',value_name='Production')
    df.insert(1,'ReportDate', report_date)
    df.insert(2,'Factory',factory)
    csv_data =df.to_csv(index=False)
    outputBlob.set(csv_data)


