import time

import requests
import streamlit as st

st.set_page_config(layout="wide")
st.title("Slussen")


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
            departures.append(
                {
                    "line": departure["line"]["designation"],
                    "destination": departure["destination"],
                    "display": departure["display"],
                    "stoppoint": departure["stop_point"]["designation"],
                }
            )
        return departures


timestamp = time.strftime("%Y%m%d%H%M")
departuredata = get_departures(timestamp)

buses = []
for departure in departuredata:
    buses.append(departure["line"])
buses = sorted(list(set(buses)))

buses_selected = st.multiselect("Välj bussar", buses, default=buses)

output = []
for departure in departuredata:
    if departure["line"] in buses_selected:
        output.append(
            {
                "Linje": departure["line"],
                "Destination": departure["destination"],
                "Avgår": departure["display"],
                "Hållplats": departure["stoppoint"],
            }
        )

st.dataframe(output, use_container_width=True)
