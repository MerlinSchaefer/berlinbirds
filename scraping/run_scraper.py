import json
import os
from datetime import datetime

import pandas as pd
from scraper import scrape_bird_data

# TODO: embed into orchestration tool

if __name__ == "__main__":
    # Example usage
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to 'urls.json' relative to the script's directory
    json_file_path = os.path.join(script_dir, "urls.json")

    try:
        with open(json_file_path, "r") as json_file:
            json_dict = json.load(json_file)
    except FileNotFoundError:
        print(f"Error: '{json_file_path}' does not exist.")

    start_url_2days = json_dict.get("start_url_2days")
    start_url_7days = json_dict.get("start_url_7days")
    data = scrape_bird_data(start_url_7days)

    # save data as parquet
    data_df = pd.DataFrame(data)
    # Current time formatted in a way that is safe for filenames
    now = datetime.now().strftime("%Y-%m-%d_%H-%M")
    # TODO: create logic to save at correct place
    data_df.to_parquet(path=f"./data/{now}_past_7_day_data.parquet")
