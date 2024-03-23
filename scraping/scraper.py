import random
import time

import requests
from bs4 import BeautifulSoup


def extract_bird_data(soup):
    data = []
    # Find all timestamps
    list_tops = soup.find_all("div", class_="listTop")
    for list_top in list_tops:
        timestamp = list_top.text.strip()  # Extract timestamp
        observation_sibling = list_top.find_next_sibling()

        # Variables to hold data that persists across siblings
        location = None

        while observation_sibling and observation_sibling.get("class") != ["listTop"]:
            classes = observation_sibling.get("class", [])

            if "listSubmenu" in classes:
                # Update location for this and subsequent observations
                location = observation_sibling.text.strip()

            elif "listObservation" in classes:
                # Proceed to extract observation data here
                count = observation_sibling.find(
                    "span"
                ).text.strip()  # Example, adjust as necessary

                # Example extraction, adjust selectors as necessary
                common_name = observation_sibling.find("b").text.strip()
                sci_name = observation_sibling.find(
                    "span", class_="sci_name"
                ).text.strip("()")

                # If the details are not directly in `listObservation`, adjust the find operation accordingly
                details = observation_sibling.find(
                    "div", class_="details_class"
                )  # Placeholder class name
                details_text = (
                    details.text.strip() if details else "No Details Available"
                )

                # Append data including location, timestamp, and details
                data.append(
                    {
                        "timestamp": timestamp,
                        "location": location,
                        "count": count,
                        "common_name": common_name,
                        "scientific_name": sci_name,
                        "details": details_text,
                    }
                )

            # Move to next sibling
            observation_sibling = observation_sibling.find_next_sibling()

    return data


def scrape_bird_data(start_url, max_pages=250):
    all_data = []
    for current_page in range(1, max_pages + 1):
        # Format the start_url with the current page number
        formatted_url = start_url.format(page_num=current_page)
        print(f"Scraping {formatted_url}")  # Debug print to track URL being requested

        response = requests.get(formatted_url, timeout=30)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            page_data = extract_bird_data(soup)
            if not page_data:
                print("No more data found. Stopping.")
                break
            all_data.extend(page_data)
            print(f"Data extracted from page {current_page}")
        else:
            print("Failed to retrieve webpage")
            break
        # Wait for 1 to 5 seconds before proceeding to the next page
        wait_secs = random.randint(1, 5)  # nosec
        print(f"waiting for {wait_secs}")
        time.sleep(wait_secs)
    return all_data
