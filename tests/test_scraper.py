from bs4 import BeautifulSoup

from scraping.scraper import extract_bird_data


def test_no_bird_observation():
    """
    Test case to verify the behavior of the `extract_bird_data` function
    when there is no bird observation in the HTML soup.

    Parameters:
    - None

    Returns:
    - None
    """
    soup = BeautifulSoup("<html><body></body></html>", "html.parser")
    assert extract_bird_data(soup) == []


def test_single_bird_observation(html_content):
    """
    Test the extraction of bird data from a single bird observation HTML page.

    Parameters:
        html_content (dict): A dictionary containing the HTML content of the single bird observation page.

    Returns:
        None

    Raises:
        AssertionError: If the extracted bird data does not match the expected result.

    """
    soup = BeautifulSoup(html_content["single_bird_observation"], "html.parser")
    expected_result = [
        {
            "timestamp": "Timestamp",
            "location": None,
            "count": "Count",
            "common_name": "Common Name",
            "scientific_name": "Scientific Name",
            "details": "Details",
        }
    ]
    assert extract_bird_data(soup) == expected_result


def test_multiple_bird_observations(html_content):
    """
    Test the functionality of extracting multiple bird observations from an HTML content.

    Parameters:
    - html_content (str): The HTML content containing multiple bird observations.

    Returns:
    - None
    """
    soup = BeautifulSoup(html_content["multiple_bird_observations"], "html.parser")
    expected_result = [
        {
            "timestamp": "Timestamp 1",
            "location": "Location 1",
            "count": "Count 1",
            "common_name": "Common Name 1",
            "scientific_name": "Scientific Name 1",
            "details": "Details 1",
        },
        {
            "timestamp": "Timestamp 2",
            "location": "Location 2",
            "count": "Count 2",
            "common_name": "Common Name 2",
            "scientific_name": "Scientific Name 2",
            "details": "Details 2",
        },
    ]
    assert extract_bird_data(soup) == expected_result
