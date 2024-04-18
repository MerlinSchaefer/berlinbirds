import json
import os
from datetime import datetime

import pandas as pd
from azure.storage.blob import BlobServiceClient
from scraper import scrape_bird_data

if __name__ == "__main__":
    # Read URLs and Azure Storage credentials from environment variables
    start_url_2days = os.getenv("START_URL_2DAYS")
    start_url_7days = os.getenv("START_URL_7DAYS")
    storage_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_CONTAINER_NAME")

    # Load URLs from JSON file if environment variables are not set
    if not start_url_2days or not start_url_7days:
        print("Environment variables not found, attempting to load from urls.json...")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(script_dir, "urls.json")

        try:
            with open(json_file_path, "r") as json_file:
                json_dict = json.load(json_file)
                start_url_2days = json_dict.get("start_url_2days")
                start_url_7days = json_dict.get("start_url_7days")
        except FileNotFoundError:
            raise Exception(f"Error: '{json_file_path}' does not exist.")

    if not start_url_2days or not start_url_7days:
        raise Exception("Failed to obtain URLs. Exiting script.")
    else:
        today_date = datetime.now().strftime("%d.%m.%Y")
        start_url_2days = start_url_2days.replace("{today}", today_date)
        start_url_7days = start_url_7days.replace("{today}", today_date)

        data = scrape_bird_data(start_url_7days)
        data_df = pd.DataFrame(data)
        now = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"{now}_past_7_day_data.parquet"
        data_df.to_parquet(path=f"scraping/scraping_data/{filename}")

        # Upload to Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(
            storage_connection_string
        )
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=filename
        )
        with open(filename, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
