import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import serial
import time
from geopy.geocoders import Nominatim

# Initialize serial port for hardware connection (e.g., for GPS and ultrasonic)
serial_port = 'COM9'  # Replace with the correct serial port
ser = serial.Serial(serial_port, 9600, timeout=1)

# Function to fetch GPS data from the serial port (e.g., GPS module)
def get_gps_data():
    # Read data from GPS sensor
    while True:
        line = ser.readline().decode('utf-8', errors='ignore')
        if line.startswith('$GPGGA'):
            gps_data = line.split(',')
            latitude = float(gps_data[2]) / 100  # Convert to decimal
            longitude = float(gps_data[4]) / 100  # Convert to decimal
            return latitude, longitude
        time.sleep(1)

# Function to fetch ultrasonic sensor data for smart parking tracking (or other sensors)
def get_parking_data():
    # Assuming the ultrasonic sensor returns a value (replace with your own sensor logic)
    # Simulating parking lot occupancy
    occupied = 10  # Sample data, replace with actual logic
    total = 20  # Total spaces in parking lot
    vacant = total - occupied
    return vacant, total

# Function to fetch location from ThingSpeak
def fetch_location_from_thingspeak():
    API_KEY = '0AKJTZTFTJL76SMD'
    CHANNEL_ID = '2769557'
    URL = f'https://api.thingspeak.com/channels/2769557/feeds.json?api_key=0AKJTZTFTJL76SMD'

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

# Streamlit App Title
st.title("Smart Parking Tracker")

# Section: Get Current Location
st.write("### Fetching Location")
latitude, longitude = get_gps_data()  # Fetch data from hardware GPS
if latitude and longitude:
    st.write(f"Current Location: Latitude {latitude}, Longitude {longitude}")
else:
    st.write("Error fetching GPS data.")

# Section: Display Location on Map
st.write("### Map View of Your Location")
m = folium.Map(location=[latitude, longitude], zoom_start=15)
folium.Marker([latitude, longitude], popup="Your Location").add_to(m)
st_folium(m, width=700, height=500)

# Section: Fetch Parking Data
vacant, total = get_parking_data()
st.write(f"Vacant Parking Spaces: {vacant}/{total}")

# Section: Send Data to IoT System (e.g., to ThingSpeak)
iot_endpoint = st.text_input("Enter IoT Endpoint URL:", "https://example-iot-cloud.com/api/coordinates")

if st.button("Send Location to IoT"):
    try:
        data = {"latitude": latitude, "longitude": longitude, "vacant_spaces": vacant}
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
