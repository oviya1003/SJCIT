import streamlit as st
from streamlit_folium import st_folium
import folium
from streamlit_js_eval import streamlit_js_eval

# Streamlit Page Configuration
st.set_page_config(page_title="Smart Parking Spot Finder", layout="centered")

# Title
st.title("Smart Parking Spot Finder 🅿️")
st.write("Click the button below to find your current location:")

# Button to Trigger Location Fetch
if st.button("Find My Location"):
    st.write("Fetching your location. Please allow access in your browser...")

    # Execute JavaScript to get the user's location
    location = streamlit_js_eval(js_code="navigator.geolocation.getCurrentPosition(position => position.coords, console.error);", key="geoLocation")

    # Show location if retrieved
    if location:
        latitude = location.get("latitude")
        longitude = location.get("longitude")
        
        if latitude and longitude:
            st.success(f"Location found: Latitude = {latitude}, Longitude = {longitude}")

            # Display map
            m = folium.Map(location=[latitude, longitude], zoom_start=15)
            folium.Marker([latitude, longitude], popup="You are here!").add_to(m)
            st.subheader("Your Location on the Map:")
            st_folium(m, width=700, height=500)
        else:
            st.error("Unable to retrieve location. Please try again.")
