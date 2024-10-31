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

# Configure Streamlit page
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


# Utility function for fetching data
def fetch_data(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error("Request timed out.")
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP error occurred: {e}")
    except RequestException as e:
        st.error(f"An error occurred: {e}")
    return None


@st.cache_data(ttl=60)
def get_departures():
    departures = []
    for site in SITES:
        url = BASE_DEPARTURE_URL.format(site=site)
        data = fetch_data(url)
        if not data:
            continue

        for departure in data.get("departures", []):
            line_designation = departure["line"]["designation"]
            if line_designation in LINES:
                stoppoint = departure.get("stop_point", {}).get("designation", "")
                if line_designation in LINES_GLASBRUKSGATAN:
                    stoppoint = "Glasbruksgatan"
                elif line_designation in LINES_SLUSSBROGATAN:
                    stoppoint += " (Slussbrogatan)"

                # Parse the expected time
                try:
                    expected_time = datetime.fromisoformat(departure["expected"])
                except ValueError:
                    expected_time = None  # Handle parsing errors if necessary

                departures.append(
                    {
                        "line": line_designation,
                        "destination": departure["destination"],
                        "display": departure["display"],
                        "expected": expected_time,
                        "stoppoint": stoppoint,
                    }
                )

    # Sort departures by expected time
    departures.sort(key=lambda x: x["expected"] or datetime.max)
    return departures


@st.cache_data(ttl=60)
def get_deviations():
    sitestring = "".join(f"&site={site}" for site in SITES)
    url = f"{BASE_DEVIATION_URL}{sitestring}"
    data = fetch_data(url)
    if not data:
        return []

    deviations = []
    for deviation in data:
        for message in deviation.get("message_variants", []):
            priority = deviation.get("priority", {})
            importance = priority.get("importance_level", 0)
            influence = priority.get("influence_level", 0)
            urgency = priority.get("urgency_level", 0)
            priority_score = importance * influence * urgency

            if priority_score > PRIORITY_THRESHOLD and message.get("language") == "sv":
                deviations.append(
                    {"header": message["header"], "details": message["details"]}
                )

    return deviations


# Fetching departures and deviations
departuredata = get_departures()
deviationdata = get_deviations()

# Display deviations if any
if deviationdata:
    with st.expander("**:red[Trafikstörningar]**", icon="🚨"):
        for deviation in deviationdata:
            st.error(f"**{deviation['header']}**")
            st.write(deviation["details"])

# Validate departure data
if not departuredata:
    st.error("Inga avgångar hittades")
    st.stop()


# Select bus lines
def bus_sort_key(line):
    digits = "".join(filter(str.isdigit, line))
    return int(digits) if digits else float("inf")


buses = sorted(
    {departure["line"] for departure in departuredata},
    key=bus_sort_key,
)

all_buses = st.checkbox(
    "Alla bussar (avmarkera för att välja enskilda linjer)", value=True
)
buses_selected = (
    buses
    if all_buses
    else st.multiselect("Välj bussar", buses, placeholder="Inga bussar valda")
)

# Validate selected bus lines
if not buses_selected:
    st.error("Inga bussar valda")
    st.stop()

# Filter and display departures
output = [
    {
        "Linje": departure["line"],
        "Destination": departure["destination"],
        "Avgår": departure["display"],
        "Hållplats": departure["stoppoint"],
    }
    for departure in departuredata
    if departure["line"] in buses_selected
]

if not output:
    st.error("Inga avgångar hittades")
    st.stop()

st.dataframe(output, use_container_width=True)
st.button("Uppdatera")
