import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# Custom styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #f0fdf4;
    }
    
    h1, h2, h3 {
        color: #047857;
    }
    
    .stButton > button {
        background-color: #10b981;
        color: white;
        font-size: 1.1rem;
    }
    
    .stButton > button:hover {
        background-color: #059669;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 3rem; margin: 0; font-weight: 900; color: #047857;">Optimal Site Map</h1>
        <p style="color: #10b981; font-size: 1.3rem;">View your recommended power plant location</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Input section
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    input_type = st.radio(
        "Input Type",
        options=["City & State", "Coordinates"],
        horizontal=True,
        label_visibility="collapsed"
    )

if input_type == "City & State":
    with col1:
        city = st.text_input("City", placeholder="e.g., Austin", key="city_input")
    with col2:
        state = st.text_input("State", placeholder="e.g., Texas", key="state_input")
    with col3:
        search_button = st.button("Search", use_container_width=True, type="primary")
    
    if search_button and city and state:
        # Convert city/state to coordinates
        try:
            geocoder = Nominatim(user_agent="renewweb_sitemap")
            address = f"{city}, {state}, USA"
            location = geocoder.geocode(address)
            
            if location:
                st.session_state.latitude = location.latitude
                st.session_state.longitude = location.longitude
                st.session_state.location_name = f"{city}, {state}"
            else:
                st.error(f"Could not find: {city}, {state}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

else:  # Coordinates input
    with col1:
        latitude_input = st.number_input("Latitude", value=30.2672, step=0.0001, format="%.4f", key="lat_input")
    with col2:
        longitude_input = st.number_input("Longitude", value=-97.7431, step=0.0001, format="%.4f", key="lon_input")
    with col3:
        search_button = st.button("Search", use_container_width=True, type="primary")
    
    if search_button:
        st.session_state.latitude = latitude_input
        st.session_state.longitude = longitude_input
        st.session_state.location_name = f"({latitude_input:.4f}, {longitude_input:.4f})"

# Get coordinates from session state
latitude = st.session_state.get("latitude")
longitude = st.session_state.get("longitude")
location_name = st.session_state.get("location_name", "Location")

st.divider()

# Display map if coordinates are available
if latitude is not None and longitude is not None:
    
    # Show coordinates info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Latitude", f"{latitude:.4f}")
    with col2:
        st.metric("Longitude", f"{longitude:.4f}")
    with col3:
        st.metric("Location", location_name if input_type == "City & State" else "Custom")
    
    st.divider()
    
    # Create and display map
    st.subheader("Power Plant Site Location")
    
    m = folium.Map(
        location=[latitude, longitude],
        zoom_start=10,
        tiles="OpenStreetMap"
    )
    
    # Add marker for the optimal site
    folium.Marker(
        location=[latitude, longitude],
        popup=f"Optimal Site: {location_name}",
        tooltip=location_name,
        icon=folium.Icon(color="green", icon="star", prefix="fa")
    ).add_to(m)
    
    # Add circle to show area of interest (50km radius)
    folium.Circle(
        location=[latitude, longitude],
        radius=50000,
        color="green",
        fill=True,
        fillColor="green",
        fillOpacity=0.1,
        popup="50km potential development area"
    ).add_to(m)
    # Display the map
    st_folium(m, use_container_width=True, height=800)
    
    st.divider()
    