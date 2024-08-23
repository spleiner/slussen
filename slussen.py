import time

import requests
import streamlit as st

st.set_page_config(layout="wide")


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

buses = list(set(buses))
buses.sort(key=lambda x: int("".join([i for i in x if i.isdigit()])))

all_buses = st.checkbox("Alla bussar", value=True)

if all_buses:
    buses_selected = buses
else:
    buses_selected = st.multiselect(
        "Välj bussar", buses, default=buses, placeholder="Inga bussar valda"
    )


output = []
if not buses_selected:
    st.error("Inga bussar valda")
    st.stop()

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
st.button("Uppdatera")
