import streamlit as st
import pandas as pd
import requests
import time


def calculate_solar_financials(irradiance, num_panels,
                               panel_area=1.7, panel_efficiency=0.18,
                               electricity_rate=0.12,
                               panel_cost=250, install_cost=250,
                               maintenance_cost=15,
                               lifetime_years=25, discount_rate=0.05):

    # Energy per panel
    annual_energy_per_panel = irradiance * panel_area * panel_efficiency * 365  # kWh/year
    total_annual_energy = annual_energy_per_panel * num_panels

    # Revenue
    annual_revenue = total_annual_energy * electricity_rate

    # Costs
    total_initial_cost = num_panels * (panel_cost + install_cost)
    total_maintenance = num_panels * maintenance_cost
    annual_net_savings = annual_revenue - total_maintenance

    # Payback Period
    payback_period = total_initial_cost / annual_net_savings if annual_net_savings > 0 else None

    # ROI %
    roi_percent = (annual_net_savings / total_initial_cost) * 100 if total_initial_cost > 0 else 0

    return {
        "Annual Energy (kWh)": total_annual_energy,
        "Annual Revenue ($)": annual_revenue,
        "Net Annual Savings ($)": annual_net_savings,
        "Total Initial Cost ($)": total_initial_cost,
        "Payback Period (years)": payback_period,
        "ROI (%)": roi_percent
    }

st.title("☀️ Top 5 US Locations for Solar Energy")

# Your API key

api_key = "TeVSdN0qrq07P3SYpVvcr8xcjvN4gVwXlk4uKmyD"

# Define cities to check
cities = {
    'Phoenix, AZ': (33.4484, -112.0740),
    'Las Vegas, NV': (36.1699, -115.1398),
    'Los Angeles, CA': (34.0522, -118.2437),
    'Albuquerque, NM': (35.0844, -106.6504),
    'Miami, FL': (25.7617, -80.1918),
    'Denver, CO': (39.7392, -104.9903),
    'Austin, TX': (30.2672, -97.7431),
    'San Diego, CA': (32.7157, -117.1611),
    'Houston, TX': (29.7604, -95.3698),
    'Seattle, WA': (47.6062, -122.3321),
    'New York, NY': (40.7128, -74.0060),
    'Chicago, IL': (41.8781, -87.6298),
    'Boston, MA': (42.3601, -71.0589),
    'Atlanta, GA': (33.7490, -84.3880),
    'Dallas, TX': (32.7767, -96.7970),
}

if st.button("🔍 Find Top 5 Solar Locations"):
    st.write("Fetching data from NREL API...")
    
    results = []
    
    # Progress bar
    progress = st.progress(0)
    
    for idx, (city, (lat, lon)) in enumerate(cities.items()):
        try:
            # API call
            url = "https://developer.nrel.gov/api/solar/solar_resource/v1.json"
            params = {
                'api_key': api_key,
                'lat': lat,
                'lon': lon
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            # Extract irradiance
            if 'outputs' in data:
                ghi = data['outputs']['avg_ghi']['annual']
                results.append({
                    'City': city,
                    'Solar Irradiance (kWh/m²/day)': float(ghi),
                    'Latitude': lat,
                    'Longitude': lon
                })
                st.write(f"✅ {city}: {ghi} kWh/m²/day")
            else:
                st.warning(f"⚠️ No data for {city}")
            
            # Update progress
            progress.progress((idx + 1) / len(cities))
            time.sleep(0.2)  # Small delay to avoid rate limiting
            
        except Exception as e:
            st.error(f"❌ Error fetching {city}: {e}")
    
    if results:
        df = pd.DataFrame(results)
        df = df.sort_values('Solar Irradiance (kWh/m²/day)', ascending=False)
        
        # Display Top 5 irradiance
        st.subheader("🏆 Top 5 Best Locations for Solar Energy")
        st.dataframe(df.head(5), use_container_width=True)

        # Ask number of panels **inside the block**
        num_panels = st.number_input(
            "🔢 Enter number of solar panels you plan to install",
            min_value=1,
            max_value=1000,
            value=10,
            step=1
        )

        # ROI Calculations
        st.subheader("💰 ROI Analysis for Top 5 Locations")
        roi_results = []
        top5 = df.head(5)
        for _, row in top5.iterrows():
            city = row['City']
            irradiance = row['Solar Irradiance (kWh/m²/day)']
            financials = calculate_solar_financials(irradiance, num_panels)
            roi_results.append({
                "City": city,
                **financials
            })

        roi_df = pd.DataFrame(roi_results)
        st.dataframe(roi_df, use_container_width=True)


# add a budget option
