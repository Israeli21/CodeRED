import streamlit as st
import pandas as pd
import requests
import time


def calculate_solar_financials(irr, panels,
                               panel_area=1.7, panel_efficiency=0.18,
                               electricity_rate=0.12,
                               panel_unit_cost=250, install_unit_cost=250,
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

# Ask user for budget
budget = st.number_input(
    "💰 Enter your total solar installation budget ($)",
    min_value=1000,
    max_value=100000,
    value=5000,
    step=500
)

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
    'Austin, TX': (30.3005, -97.7522),
    'San Diego, CA': (32.7157, -117.1611),
    'Houston, TX': (29.7604, -95.3698),
    'Seattle, WA': (47.6062, -122.3321),
    'New York, NY': (40.7128, -74.0060),
    'Chicago, IL': (41.8781, -87.6298),
    'Boston, MA': (42.3601, -71.0589),
    'Atlanta, GA': (33.7490, -84.3880),
    'Dallas, TX': (32.7767, -96.7970),
}

# --- Define cities grouped by region ---
regions = {
    "Southwest": {
        'Phoenix, AZ': (33.4484, -112.0740),
        'Las Vegas, NV': (36.1699, -115.1398),
        'Albuquerque, NM': (35.0844, -106.6504),
    },
    "West Coast": {
        'Los Angeles, CA': (34.0522, -118.2437),
        'San Diego, CA': (32.7157, -117.1611),
        'Seattle, WA': (47.6062, -122.3321),
    },
    "South": {
        'Miami, FL': (25.7617, -80.1918),
        'Atlanta, GA': (33.7490, -84.3880),
        'Dallas, TX': (32.7767, -96.7970),
        'Austin, TX': (30.3005, -97.7522),
        'Houston, TX': (29.7604, -95.3698),
    },
    "Midwest": {
        'Chicago, IL': (41.8781, -87.6298),
    },
    "Northeast": {
        'New York, NY': (40.7128, -74.0060),
        'Boston, MA': (42.3601, -71.0589),
    }
}

# --- Create a combined "All" option ---
regions["All"] = {}
for region_dict in regions.values():
    if isinstance(region_dict, dict):  # skip "All" itself during iteration
        regions["All"].update(region_dict)

# --- Streamlit selection ---
region_selected = st.selectbox("Select a region", options=list(regions.keys()))

# --- Get the cities for that region ---
selected_cities = regions[region_selected]

st.write(f"### Cities in {region_selected}")
for city, (lat, lng) in selected_cities.items():
    st.write(f"{city}: {lat}, {lng}")

if st.button("🔍 Find Top 5 Solar Locations"):
    st.write("Fetching data from NREL API...")

    results = []
    progress = st.progress(0)

    for idx, (city, (lat, lon)) in enumerate(selected_cities.items()):  # <-- use selected_cities here
        try:
            url = "https://developer.nrel.gov/api/solar/solar_resource/v1.json"
            params = {
                'api_key': api_key,
                'lat': lat,
                'lon': lon
            }

            response = requests.get(url, params=params)
            data = response.json()

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

            progress.progress((idx + 1) / len(selected_cities))
            time.sleep(0.2)

        except Exception as e:
            st.error(f"❌ Error fetching {city}: {e}")

    if results:
        df = pd.DataFrame(results)
        df = df.sort_values('Solar Irradiance (kWh/m²/day)', ascending=False)
        
        # Display Top 5 irradiance
        st.subheader("🏆 Top 5 Best Locations for Solar Energy")
        st.dataframe(df.head(5),  width='stretch')


        # ROI Calculations
        st.subheader("💰 ROI Analysis Based on Your Budget")
        roi_results = []
        panel_cost = 250
        install_cost = 250
        total_cost_per_panel = panel_cost + install_cost

        top5 = df.head(5)
        for _, row in top5.iterrows():
            city = row['City']
            irradiance = row['Solar Irradiance (kWh/m²/day)']

            # Calculate number of panels based on budget
            num_panels = budget // total_cost_per_panel
            if num_panels < 1:
                num_panels = 1

            financials = calculate_solar_financials(irradiance, num_panels)
            roi_results.append({
                "City": city,
                "Number of Panels": int(num_panels),
                **financials
            })

        roi_df = pd.DataFrame(roi_results)
        roi_df = roi_df.sort_values("Net Annual Savings ($)", ascending=False)
        st.dataframe(roi_df, width='stretch')

        # Highlight the best location for the budget
        best = roi_df.iloc[0]
        st.success(f"🏆 Best Location for a ${budget} Budget: **{best['City']}** with {best['Number of Panels']} panels")

# add a budget option
