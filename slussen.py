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
    headers = {"Content-Type": "application/json"}
    url = "https://transport.integration.sl.se/v1/sites/9192/departures?transport=BUS"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
    else:
        return None

    if data:
        for departure in data["departures"]:
            if (
                len(departure["line"]["designation"]) >= 3
                and departure["line"]["designation"][:3].isdigit()
                and departure["line"]["designation"][:1] == "4"
            ):
                departures.append(
                    {
                        "line": departure["line"]["designation"],
                        "destination": departure["destination"],
                        "display": departure["display"],
                        "stoppoint": departure["stop_point"]["designation"],
                    }
                )
        return departures
    else:
        return None


timestamp = time.strftime("%Y%m%d%H%M")
departuredata = get_departures(timestamp)

buses = sorted(
    {departure["line"] for departure in departuredata},
    key=lambda x: int("".join(filter(str.isdigit, x))),
)

all_buses = st.checkbox("Alla bussar", value=True)
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
