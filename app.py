import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

# Streamlit App Title
st.title("Smart Parking Tracker")

# Section: Get Current Location
if st.button("Get Current Location"):
    st.write("Fetching location...")

    # JavaScript to fetch geolocation data
    loc_script = """
    <script>
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const coords = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                };
                document.getElementById("location-data").innerText = JSON.stringify(coords);
            },
            (error) => {
                document.getElementById("location-data").innerText = "Error: Unable to fetch location.";
            }
        );
    </script>
    <div id="location-data">Waiting for location...</div>
    """
    result = st.components.v1.html(loc_script, height=100)
    
    # Parse the JavaScript result
    if result:
        try:
            location_data = eval(result)
            latitude = location_data.get("latitude", 0)
            longitude = location_data.get("longitude", 0)
            st.write(f"Current Location: Latitude {latitude}, Longitude {longitude}")
        except Exception:
            st.write("Error fetching location. Please try again.")

# Example fetched coordinates (fallback for demonstration)
latitude, longitude = 13.394968, 77.728851  # Replace with real fetched data when working

# Section: Display Location on Map
st.write("### Map View of Your Location")
m = folium.Map(location=[latitude, longitude], zoom_start=15)
folium.Marker([latitude, longitude], popup="Your Location").add_to(m)
st_folium(m, width=700, height=500)

# Section: Send Coordinates to IoT System
st.write("### Integrating with IoT System")
iot_endpoint = st.text_input("Enter IoT Endpoint URL:", "https://example-iot-cloud.com/api/coordinates")

if st.button("Send Location to IoT"):
    try:
        data = {"latitude": latitude, "longitude": longitude}
        response = requests.post(iot_endpoint, json=data)
        if response.status_code == 200:
            st.success("Location sent successfully!")
            st.write("Response:", response.json())
        else:
            st.error(f"Failed to send location. Status code: {response.status_code}")
            st.write("Response:", response.text)
    except Exception as e:
        st.error("Error sending location to IoT system.")
        st.write(e)






import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import time

# Streamlit App Title
st.title("Smart Parking Tracker")

# ThingSpeak API Details
API_KEY = '0AKJTZTFTJL76SMD'
CHANNEL_ID = '2769557'
URL = f'https://api.thingspeak.com/channels/2769557/feeds.json?api_key=0AKJTZTFTJL76SMD'

# Fetch Location from ThingSpeak
def fetch_location():
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            latest_data = data['feeds'][-1]  # Get the most recent data
            latitude = float(latest_data['field1'])
            longitude = float(latest_data['field2'])
            return latitude, longitude
        else:
            st.error("Error fetching data from ThingSpeak!")
            return None, None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None

# Section: Display Location on Map
latitude, longitude = fetch_location()

if latitude and longitude:
    st.write("### Map View of Your Location")
    # Display the map with fetched coordinates
    m = folium.Map(location=[latitude, longitude], zoom_start=15)
    folium.Marker([latitude, longitude], popup="Your Location").add_to(m)
    st_folium(m, width=700, height=500)

    # Section: Send Coordinates to IoT System
    st.write("### Integrating with IoT System")
    iot_endpoint = st.text_input("Enter IoT Endpoint URL:", "https://example-iot-cloud.com/api/coordinates")

    if st.button("Send Location to IoT"):
        try:
            data = {"latitude": latitude, "longitude": longitude}
            response = requests.post(iot_endpoint, json=data)
            if response.status_code == 200:
                st.success("Location sent successfully!")
                st.write("Response:", response.json())
            else:
                st.error(f"Failed to send location. Status code: {response.status_code}")
                st.write("Response:", response.text)
        except Exception as e:
            st.error("Error sending location to IoT system.")
            st.write(e)

else:
    st.write("Fetching data from ThingSpeak...")
    st.spinner("Please wait...")  # Show a loading spinner while fetching location
    time.sleep(5)  # Simulate waiting time for data fetch (use appropriate logic)
