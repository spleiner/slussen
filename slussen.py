from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

import requests
import streamlit as st
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, RequestException, Timeout
from urllib3.util.retry import Retry

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
REQUEST_TIMEOUT_SECONDS = 10
CACHE_TTL_SECONDS = 60


# Configure Streamlit page
def configure_page() -> None:
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
        },  # pyright: ignore[reportArgumentType]
    )


# Utility function for fetching data with retry mechanism
@st.cache_resource
def get_http_session() -> requests.Session:
    """Create a shared HTTP session with retry strategy."""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def fetch_json(url: str) -> Any:
    """Fetch JSON data from a given URL with robust error handling."""
    session = get_http_session()
    try:
        response = session.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json()
    except Timeout as exc:
        raise Timeout("Request timed out.") from exc
    except HTTPError as exc:
        raise HTTPError(f"HTTP error: {exc}") from exc
    except RequestException as exc:
        raise RequestException(f"Request error: {exc}") from exc


# Function to fetch departure data concurrently
@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def fetch_departure_data() -> List[Dict[str, Any]]:
    """
    Fetch and parse departure information for all specified sites.
    """
    departures = []

    def fetch_and_parse(site: str) -> List[Dict[str, Any]]:
        url = BASE_DEPARTURE_URL.format(site=site)
        try:
            data = fetch_json(url)
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
def parse_departure_data(data: Any) -> List[Dict[str, Any]]:
    """
    Parse departure data from the API response.
    """
    departures = []
    if not isinstance(data, dict):
        return departures

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
            st.toast(f"Missing key in departure data: {e}", icon="⚠️")
        except Exception as e:
            st.toast(f"Error parsing departure data: {e}", icon="❗")
    return departures


# Function to determine stop point
def get_stop_point(departure: Dict[str, Any], line_designation: str) -> str:
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
@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def fetch_deviation_data() -> List[Dict[str, str]]:
    """
    Fetch and parse deviation messages for the specified sites.
    """
    deviations = []

    def fetch_and_parse(site: str) -> List[Dict[str, str]]:
        url = f"{BASE_DEVIATION_URL}&site={site}"
        try:
            data = fetch_json(url)
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
def parse_deviation_data(data: Any) -> List[Dict[str, str]]:
    """
    Parse deviation messages from the API response.
    """
    deviations = []
    if not isinstance(data, list):
        return deviations

    for deviation in data:
        try:
            for message in deviation.get("message_variants", []):
                if should_include_deviation(deviation, message):
                    deviations.append(
                        {"header": message["header"], "details": message["details"]}
                    )
        except KeyError as e:
            st.toast(f"Missing key in deviation data: {e}", icon="⚠️")
        except Exception as e:
            st.toast(f"Error parsing deviation data: {e}", icon="❗")
    return deviations


# Function to determine if a deviation should be included
def should_include_deviation(
    deviation: Dict[str, Any], message: Dict[str, Any]
) -> bool:
    """
    Determine if the deviation message should be included based on priority score and language.
    """
    priority_score = calculate_priority_score(deviation.get("priority", {}))
    return priority_score > PRIORITY_THRESHOLD and message.get("language") == "sv"


# Function to parse the expected time
def parse_expected_time(expected_time_str: Optional[str]) -> Optional[datetime]:
    """
    Parse the expected time from a string, returning None if parsing fails.
    """
    if not expected_time_str:
        return None
    try:
        normalized = expected_time_str.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    except (ValueError, TypeError):
        return None


# Function to calculate the priority score
def calculate_priority_score(priority_data: Dict[str, Any]) -> int:
    """
    Calculate the priority score from the priority dictionary.
    """
    importance = priority_data.get("importance_level", 0)
    influence = priority_data.get("influence_level", 0)
    urgency = priority_data.get("urgency_level", 0)
    return importance * influence * urgency


# Function to display deviations
def display_deviations(deviation_data: List[Dict[str, str]]) -> None:
    """
    Display traffic deviations using Streamlit.
    """
    if deviation_data:
        st.subheader("Trafikstörningar")
        for deviation in deviation_data:
            st.error(f"🚨 {deviation['header']}")
            st.write(deviation["details"])


# Function to validate departure data
def validate_departure_data(departure_data: List[Dict[str, Any]]) -> bool:
    """
    Validate the departure data and show warning if none are found.
    """
    if not departure_data:
        st.warning("Inga avgångar hittades. Försök hämta data igen.")
        return False
    return True


# Function to get bus lines
def get_sorted_bus_lines(departure_data: List[Dict[str, Any]]) -> List[str]:
    """
    Get a sorted list of bus lines from departure data.
    """
    bus_lines = sorted(
        {departure["line"] for departure in departure_data},
        key=get_bus_sort_key,
    )
    return bus_lines


# Function to get the sort key for bus lines
def get_bus_sort_key(line: str) -> float:
    """
    Extract numeric value from line for sorting purposes.
    """
    digits = "".join(filter(str.isdigit, line))
    return int(digits) if digits else float("inf")


# Function to filter selected bus lines
def filter_departures_by_selected_lines(
    departure_data: List[Dict[str, Any]],
    selected_bus_lines: Iterable[str],
) -> List[Dict[str, str]]:
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
def main() -> None:
    configure_page()

    st.title("SLussen")

    # Initialize session state for data
    if "departure_data" not in st.session_state:
        st.session_state.departure_data = []
    if "deviation_data" not in st.session_state:
        st.session_state.deviation_data = []
    if "last_update" not in st.session_state:
        st.session_state.last_update = None

    # Initial fetch if no data
    if not st.session_state.departure_data:
        with st.spinner("Hämtar avgångar och trafikstörningar..."):
            st.session_state.departure_data = fetch_departure_data()
            st.session_state.deviation_data = fetch_deviation_data()
            st.session_state.last_update = datetime.now()

    departure_data = st.session_state.departure_data
    deviation_data = st.session_state.deviation_data

    # Display deviations
    display_deviations(deviation_data)

    # Validate departure data
    if not validate_departure_data(departure_data):
        return

    # Main content
    st.subheader("Avgångar")
    if st.session_state.last_update:
        st.caption(
            f"Senast uppdaterad: {st.session_state.last_update.strftime('%H:%M:%S')}"
        )

    # Select bus lines
    bus_lines = get_sorted_bus_lines(departure_data)
    with st.sidebar:
        st.header("Filter")
        all_bus_lines = st.toggle(
            "Alla bussar (avmarkera för att välja enskilda linjer)", value=True
        )
        selected_bus_lines = (
            bus_lines
            if all_bus_lines
            else st.multiselect(
                "Välj bussar", bus_lines, placeholder="Inga bussar valda"
            )
        )

    # Validate selected bus lines
    if not selected_bus_lines:
        st.toast("Inga bussar valda", icon="⚠️")
        st.stop()

    if selected_bus_lines:
        # Filter and display departures
        filtered_departures = filter_departures_by_selected_lines(
            departure_data, selected_bus_lines
        )

        if not filtered_departures:
            st.toast("Inga avgångar hittades", icon="⚠️")
            st.stop()

        # Display the output in a table format
        st.dataframe(filtered_departures, width="stretch")

        # Update button
        if st.button("Uppdatera data"):
            with st.spinner("Hämtar avgångar och trafikstörningar..."):
                st.session_state.departure_data = fetch_departure_data()
                st.session_state.deviation_data = fetch_deviation_data()
                st.session_state.last_update = datetime.now()
                st.rerun()  # To refresh the display
    else:
        st.info("Välj bussar för att visa avgångar.")


if __name__ == "__main__":
    main()
