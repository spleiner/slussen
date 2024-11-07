import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import requests
import streamlit as st
from requests.exceptions import RequestException

# Constants
SITES = ["9192", "1321"]
HEADERS = {"Content-Type": "application/json"}
LINES = {
    "401",
    "402",
    "409",
    "410",
    "413",
    "414",
    "420",
    "422",
    "425",
    "428X",
    "429X",
    "430X",
    "432",
    "433",
    "434",
    "435",
    "436",
    "437",
    "438",
    "439",
    "440",
    "441",
    "442",
    "443",
    "444",
    "445",
    "471",
    "474",
    "491",
    "496",
    "497",
    "25M",
    "26M",
    "423",
    "449",
    "71T",
}
LINES_GLASBRUKSGATAN = {"25M", "26M", "423", "449"}
LINES_SLUSSBROGATAN = {"71T"}
BASE_DEPARTURE_URL = (
    "https://transport.integration.sl.se/v1/sites/{site}/departures?transport=BUS"
)
BASE_DEVIATION_URL = "https://deviations.integration.sl.se/v1/messages?future=true"
PRIORITY_THRESHOLD = 35
MAX_RETRIES = 3
RETRY_DELAY = 5


# Configure Streamlit page
def configure_page():
    """
    Configure the Streamlit page settings.
    """
    st.set_page_config(
        page_title="SLussen",
        page_icon="🚌",
        layout="wide",
        menu_items={
            "about": """
            # SLussen

            SLussen är en enkel app för att visa avgångar från Slussen. Appen använder SLs öppna API för att hämta data om avgångar från Slussen.
            """,
            "Report a Bug": "https://github.com/spleiner/slussen/issues",
        },
    )


# Utility function for fetching data with retry mechanism
def fetch_data_with_retries(url):
    """
    Fetch data from a given URL and return JSON.
    Includes retry mechanism for handling transient errors.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            st.warning(f"Request timed out. Retrying {attempt}/{MAX_RETRIES}...")
        except requests.exceptions.HTTPError as http_error:
            st.error(
                f"HTTP error occurred: {http_error}. Retrying {attempt}/{MAX_RETRIES}..."
            )
        except RequestException as request_error:
            st.error(
                f"An error occurred: {request_error}. Retrying {attempt}/{MAX_RETRIES}..."
            )
        time.sleep(RETRY_DELAY)
    raise Exception("Failed to fetch data after multiple attempts.")


# Function to fetch departure data concurrently
@st.cache_data(ttl=60)
def fetch_departure_data():
    """
    Fetch and parse departure information for all specified sites.
    """
    departures = []

    def fetch_and_parse(site):
        url = BASE_DEPARTURE_URL.format(site=site)
        try:
            data = fetch_data_with_retries(url)
            return parse_departure_data(data)
        except Exception as e:
            st.error(f"Error fetching data for site {site}: {e}")
            return []

    with ThreadPoolExecutor() as executor:
        results = executor.map(fetch_and_parse, SITES)

    for result in results:
        departures.extend(result)

    # Sort departures by expected time, putting None values at the end
    departures.sort(key=lambda x: x["expected"] or datetime.max)
    return departures


# Function to parse departure data
def parse_departure_data(data):
    """
    Parse departure data from the API response.
    """
    departures = []
    for departure in data.get("departures", []):
        try:
            line_designation = departure["line"]["designation"]
            if line_designation in LINES:
                stop_point = get_stop_point(departure, line_designation)
                expected_time = parse_expected_time(departure.get("expected"))
                departures.append(
                    {
                        "line": line_designation,
                        "destination": departure["destination"],
                        "display": departure["display"],
                        "expected": expected_time,
                        "stop_point": stop_point,
                    }
                )
        except KeyError as e:
            st.warning(f"Missing key in departure data: {e}")
        except Exception as e:
            st.error(f"Error parsing departure data: {e}")
    return departures


# Function to determine stop point
def get_stop_point(departure, line_designation):
    """
    Determine the correct stop point based on line designation.
    """
    stop_point = departure.get("stop_point", {}).get("designation", "")
    if line_designation in LINES_GLASBRUKSGATAN:
        stop_point = "Glasbruksgatan"
    elif line_designation in LINES_SLUSSBROGATAN:
        stop_point += " (Slussbrogatan)"
    return stop_point


# Function to fetch deviation data concurrently
@st.cache_data(ttl=60)
def fetch_deviation_data():
    """
    Fetch and parse deviation messages for the specified sites.
    """
    deviations = []

    def fetch_and_parse(site):
        url = f"{BASE_DEVIATION_URL}&site={site}"
        try:
            data = fetch_data_with_retries(url)
            return parse_deviation_data(data)
        except Exception as e:
            st.error(f"Error fetching deviations for site {site}: {e}")
            return []

    with ThreadPoolExecutor() as executor:
        results = executor.map(fetch_and_parse, SITES)

    for result in results:
        deviations.extend(result)

    return deviations


# Function to parse deviation data
def parse_deviation_data(data):
    """
    Parse deviation messages from the API response.
    """
    deviations = []
    for deviation in data:
        try:
            for message in deviation.get("message_variants", []):
                if should_include_deviation(deviation, message):
                    deviations.append(
                        {"header": message["header"], "details": message["details"]}
                    )
        except KeyError as e:
            st.warning(f"Missing key in deviation data: {e}")
        except Exception as e:
            st.error(f"Error parsing deviation data: {e}")
    return deviations


# Function to determine if a deviation should be included
def should_include_deviation(deviation, message):
    """
    Determine if the deviation message should be included based on priority score and language.
    """
    priority_score = calculate_priority_score(deviation.get("priority", {}))
    return priority_score > PRIORITY_THRESHOLD and message.get("language") == "sv"


# Function to parse the expected time
def parse_expected_time(expected_time_str):
    """
    Parse the expected time from a string, returning None if parsing fails.
    """
    try:
        return datetime.fromisoformat(expected_time_str)
    except (ValueError, TypeError):
        return None


# Function to calculate the priority score
def calculate_priority_score(priority_data):
    """
    Calculate the priority score from the priority dictionary.
    """
    importance = priority_data.get("importance_level", 0)
    influence = priority_data.get("influence_level", 0)
    urgency = priority_data.get("urgency_level", 0)
    return importance * influence * urgency


# Function to display deviations
def display_deviations(deviation_data):
    """
    Display traffic deviations using Streamlit.
    """
    if deviation_data:
        with st.expander("**:red[Trafikstörningar]**", icon="🚨"):
            for deviation in deviation_data:
                st.error(f"**{deviation['header']}**")
                st.write(deviation["details"])


# Function to validate departure data
def validate_departure_data(departure_data):
    """
    Validate the departure data and stop the app if none are found.
    """
    if not departure_data:
        st.error("Inga avgångar hittades")
        st.stop()


# Function to get bus lines
def get_sorted_bus_lines(departure_data):
    """
    Get a sorted list of bus lines from departure data.
    """
    bus_lines = sorted(
        {departure["line"] for departure in departure_data},
        key=get_bus_sort_key,
    )
    return bus_lines


# Function to get the sort key for bus lines
def get_bus_sort_key(line):
    """
    Extract numeric value from line for sorting purposes.
    """
    digits = "".join(filter(str.isdigit, line))
    return int(digits) if digits else float("inf")


# Function to filter selected bus lines
def filter_departures_by_selected_lines(departure_data, selected_bus_lines):
    """
    Filter the departure data based on selected bus lines.
    """
    return [
        {
            "Linje": departure["line"],
            "Destination": departure["destination"],
            "Avgår": departure["display"],
            "Hållplats": departure["stop_point"],
        }
        for departure in departure_data
        if departure["line"] in selected_bus_lines
    ]


# Main script
def main():
    configure_page()

    # Fetching departures and deviations
    departure_data = fetch_departure_data()
    deviation_data = fetch_deviation_data()

    # Display deviations
    display_deviations(deviation_data)

    # Validate departure data
    validate_departure_data(departure_data)

    # Select bus lines
    bus_lines = get_sorted_bus_lines(departure_data)
    all_bus_lines = st.checkbox(
        "Alla bussar (avmarkera för att välja enskilda linjer)", value=True
    )
    selected_bus_lines = (
        bus_lines
        if all_bus_lines
        else st.multiselect("Välj bussar", bus_lines, placeholder="Inga bussar valda")
    )

    # Validate selected bus lines
    if not selected_bus_lines:
        st.error("Inga bussar valda")
        st.stop()

    # Filter and display departures
    filtered_departures = filter_departures_by_selected_lines(
        departure_data, selected_bus_lines
    )

    if not filtered_departures:
        st.error("Inga avgångar hittades")
        st.stop()

    # Display the output in a table format
    st.dataframe(filtered_departures, use_container_width=True)
    st.button("Uppdatera")


if __name__ == "__main__":
    main()
