import requests
import streamlit as st

s = requests.Session()

sites = ["9192", "1321"]
headers = {"Content-Type": "application/json"}

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

LINES = [
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
]
LINES_GLASBRUKSGATAN = ["25M", "26M", "423", "449"]
LINES_SLUSSBROGATAN = ["71T"]


def fetch_data(url):
    response = s.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None


@st.cache_data(ttl=60)
def get_departures():
    departures = []
    for site in sites:
        url = f"https://transport.integration.sl.se/v1/sites/{site}/departures?transport=BUS"
        data = fetch_data(url)
        if not data:
            return departures

        for departure in data["departures"]:
            if departure["line"]["designation"] in LINES:
                stoppoint = departure.get("stop_point", {}).get("designation", "")
                if departure["line"]["designation"] in LINES_GLASBRUKSGATAN:
                    stoppoint = "Glasbruksgatan"
                elif departure["line"]["designation"] in LINES_SLUSSBROGATAN:
                    stoppoint += " (Slussbrogatan)"

                departures.append(
                    {
                        "line": departure["line"]["designation"],
                        "destination": departure["destination"],
                        "display": departure["display"],
                        "expected": departure["expected"],
                        "stoppoint": stoppoint,
                    }
                )

    return sorted(departures, key=lambda x: x["expected"])


@st.cache_data(ttl=60)
def get_deviations():
    sitestring = "".join(f"&site={site}" for site in sites)
    url = f"https://deviations.integration.sl.se/v1/messages?future=true{sitestring}"
    data = fetch_data(url)
    if not data:
        return []

    deviations = []
    for deviation in data:
        for message in deviation["message_variants"]:
            priority = deviation["priority"]
            if (
                priority["importance_level"]
                * priority["influence_level"]
                * priority["urgency_level"]
                > 35
            ) and message["language"] == "sv":
                deviations.append(
                    {"header": message["header"], "details": message["details"]}
                )

    return deviations


departuredata = get_departures()
deviationdata = get_deviations()

if deviationdata:
    with st.expander("**:red[Trafikstörningar]**", icon="🚨"):
        for deviation in deviationdata:
            st.error(f"**{deviation['header']}**")
            st.write(deviation["details"])

if not departuredata:
    st.error("Inga avgångar hittades")
    st.stop()

buses = sorted(
    {departure["line"] for departure in departuredata},
    key=lambda x: int("".join(filter(str.isdigit, x))),
)

all_buses = st.toggle(
    "Alla bussar (avmarkera för att välja enskilda linjer)", value=True
)
buses_selected = (
    buses
    if all_buses
    else st.multiselect("Välj bussar", buses, placeholder="Inga bussar valda")
)

if not buses_selected:
    st.error("Inga bussar valda")
    st.stop()

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
