import random
import time
from typing import Optional

import requests
from bs4 import BeautifulSoup


def extract_bird_data(soup: BeautifulSoup) -> list[dict[str, str]]:
    """
    Extracts bird observation data from a BeautifulSoup object parsed from HTML content.

    This function navigates through the structured HTML to find and compile a list of bird observations,
    including timestamps, locations, counts, common names, scientific names, and additional details.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object containing parsed HTML content.

    Returns:
        list[dict[str, str]]: A list of dictionaries, each representing a bird observation with keys for timestamp,
                               location, count, common name, scientific name, and details.
    """
    data = []
    list_tops = soup.find_all("div", class_="listTop")
    for list_top in list_tops:
        timestamp = list_top.text.strip()
        observation_sibling = list_top.find_next_sibling()

        location = None

        while observation_sibling and observation_sibling.get("class") != ["listTop"]:
            classes = observation_sibling.get("class", [])

            if "listSubmenu" in classes:
                location = observation_sibling.text.strip()

            elif "listObservation" in classes:
                count = observation_sibling.find("span").text.strip()
                common_name = observation_sibling.find("b").text.strip()
                sci_name = observation_sibling.find(
                    "span", class_="sci_name"
                ).text.strip("()")
                details = observation_sibling.find("div", class_="details_class")
                details_text = (
                    details.text.strip() if details else "No Details Available"
                )

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

            observation_sibling = observation_sibling.find_next_sibling()

    return data


def scrape_bird_data(
    start_url: str, max_pages: Optional[int] = 250
) -> list[dict[str, str]]:
    """
    Scrapes bird data from a specified URL up to a maximum number of pages.

    This function iterates through pages of a website, scraping bird observation data by parsing HTML content
    into a BeautifulSoup object and extracting relevant data with `extract_bird_data`.

    Args:
        start_url (str): The URL to start scraping from, with a placeholder for pagination (page_num).
        max_pages (int, optional): The maximum number of pages to scrape. Defaults to 250.

    Returns:
        list[dict[str, str]]: A list of dictionaries containing bird observation data across all scraped pages.
    """
    all_data = []
    for current_page in range(1, max_pages + 1):
        formatted_url = start_url.format(page_num=current_page)
        print(f"Scraping {formatted_url}")

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

        wait_secs = random.randint(1, 5)  # nosec
        print(f"Waiting for {wait_secs} seconds.")
        time.sleep(wait_secs)

    return all_data
