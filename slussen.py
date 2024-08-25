import time

import requests
import streamlit as st

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


@st.cache_data
def get_departures(timestamp):
    departures = []
    sites = ["9192", "1321"]
    s = requests.Session()
    for site in sites:
        headers = {"Content-Type": "application/json"}
        url = f"https://transport.integration.sl.se/v1/sites/{site}/departures?transport=BUS"
        response = s.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
        else:
            return departures

        if data:
            lines = [
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
            lines_glasbruksgatan = ["25M", "26M", "423", "449"]
            lines_slussbrogatan = ["71T"]
            for departure in data["departures"]:
                if departure["line"]["designation"] in lines:
                    departureinfo = {
                        "line": departure["line"]["designation"],
                        "destination": departure["destination"],
                        "display": departure["display"],
                        "expected": departure["expected"],
                    }
                    try:
                        departureinfo["stoppoint"] = departure["stop_point"][
                            "designation"
                        ]
                    except KeyError:
                        departureinfo["stoppoint"] = ""

                    if departure["line"]["designation"] in lines_glasbruksgatan:
                        departureinfo["stoppoint"] = "Glasbruksgatan"
                    elif departure["line"]["designation"] in lines_slussbrogatan:
                        departureinfo["stoppoint"] += " (Slussbrogatan)"

                    departures.append(departureinfo)
        else:
            return departures

    departures = sorted(departures, key=lambda x: x["expected"])
    return departures


@st.cache_data
def get_deviations(timestamp):
    deviations = []
    sites = ["9192", "1321"]
    sitestring = ""
    for site in sites:
        sitestring += f"&site={site}"
    headers = {"Content-Type": "application/json"}
    url = f"https://deviations.integration.sl.se/v1/messages?future=true{sitestring}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for deviation in data:
            for message in deviation["message_variants"]:
                if message["language"] == "sv":
                    deviationinfo = {
                        "header": message["header"],
                        "details": message["details"],
                    }
                    deviations.append(deviationinfo)
    else:
        return deviations

    return deviations


timestamp = time.strftime("%Y%m%d%H%M")
departuredata = get_departures(timestamp)
deviationdata = get_deviations(timestamp)

if deviationdata:
    with st.expander("Trafikstörningar"):
        for deviation in deviationdata:
            st.error(f"**{deviation['header']}**")
            st.write(deviation["details"])


if departuredata == []:
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
