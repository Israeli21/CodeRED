import streamlit as st
import pandas as pd
import requests
import time
import os
from dotenv import load_dotenv
# Load .env file
load_dotenv()


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

st.title("Top 5 US Locations for Solar Energy")

# --- LOAD CITIES FROM CSV ---
@st.cache_data
def load_cities_from_csv(file_path):
    """Load cities from CSV file"""
    try:
        df = pd.read_csv(file_path)
        st.success(f"✅ Loaded {len(df)} cities from CSV")
        return df
    except Exception as e:
        st.error(f"❌ Error loading CSV: {e}")
        return None

# Ask user for budget
budget = st.number_input(
    "💰 Enter your total solar installation budget ($)",
    min_value=1000,
    max_value=100000,
    value=5000,
    step=500
)

# Get API key
api_key = os.getenv("NREL_API_KEY")

if not api_key:
    st.error("API key not found! Please check your .env file.")

# Load the CSV
csv_path = "renewable_energies/cleaned_locations_with_region_new.csv"
cities_df = load_cities_from_csv(csv_path)

if cities_df is not None:
    # --- GROUP BY REGION ---
    # Assuming your CSV has columns: 'City', 'State', 'Region', 'Latitude', 'Longitude'
    # Adjust column names based on your actual CSV structure

    # Get unique regions
    if 'Region' in cities_df.columns:
        regions_list = ['All'] + sorted(cities_df['Region'].unique().tolist())
    else:
        # If no Region column, use State
        regions_list = ['All'] + sorted(cities_df['State'].unique().tolist())
        cities_df['Region'] = cities_df['State']  # Use state as region

    # --- Streamlit selection ---
    region_selected = st.selectbox("Select a region", options=regions_list)

    # Filter cities based on selection
    if region_selected == 'All':
        selected_cities_df = cities_df
    else:
        selected_cities_df = cities_df[cities_df['Region'] == region_selected]

    st.write(f"### Cities in {region_selected}: {len(selected_cities_df)} locations")

    # Optional: Let user limit number of cities to check (to save API calls)
    max_cities = st.slider(
        "Maximum cities to analyze (to avoid rate limits)",
        min_value=5,
        max_value=min(50, len(selected_cities_df)),
        value=min(15, len(selected_cities_df))
    )

    # Take only first N cities
    selected_cities_df = selected_cities_df.head(max_cities)

    # Display selected cities
    with st.expander(f"View {len(selected_cities_df)} selected cities"):
        st.dataframe(selected_cities_df)

    if st.button("Analyze Location & ROI"):
        st.write("Fetching data from NREL API...")

        results = []
        progress = st.progress(0)

        # Iterate through CSV rows
        for idx, row in selected_cities_df.iterrows():
            try:

                city = row['city']
                state = row['state_name'] if 'state_name' in row else ''
                lat = row['lat']
                lon = row['lng']

                city_label = f"{city}, {state}" if state else city

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
                        'State': state,
                        'Solar Irradiance (kWh/m²/day)': float(ghi),
                        'Latitude': lat,
                        'Longitude': lon
                    })
                    st.write(f"✅ {city_label}: {ghi} kWh/m²/day")
                else:
                    st.warning(f"⚠️ No data for {city_label}")

                for i, (_, city_row) in enumerate(selected_cities_df.iterrows()):
                    city = city_row['city']
                    state = city_row['state_name'] if 'state_name' in city_row else ''
                    lat = city_row['lat']
                    lon = city_row['lng']

                    # Update progress
                    progress.progress((i + 1) / len(selected_cities_df))
                time.sleep(0.2)  # Avoid rate limiting

            except Exception as e:
                st.error(f"❌ Error fetching: {e}")

        if results:
            df = pd.DataFrame(results)
            df = df.sort_values('Solar Irradiance (kWh/m²/day)', ascending=False)

            # Display Top 5 irradiance
            st.subheader("🏆 Top 5 Best Locations for Solar Energy")
            st.dataframe(df.head(5), width='stretch')

            # ROI Calculations
            st.subheader("ROI Analysis Based on Your Budget")
            roi_results = []
            panel_cost = 250
            install_cost = 250
            total_cost_per_panel = panel_cost + install_cost

            top5 = df.head(5)
            for _, row in top5.iterrows():
                city = row['City']
                state = row['State']
                irradiance = row['Solar Irradiance (kWh/m²/day)']

                # Calculate number of panels based on budget
                num_panels = budget // total_cost_per_panel
                if num_panels < 1:
                    num_panels = 1

                financials = calculate_solar_financials(irradiance, num_panels)
                roi_results.append({
                    "City": city,
                    "Number of Panels": int(num_panels),
                    "State": state,
                    **financials
                })

            roi_df = pd.DataFrame(roi_results)
            roi_df = roi_df.sort_values("Net Annual Savings ($)", ascending=False)
            st.dataframe(roi_df, width='stretch')

            # Highlight the best location for the budget
            best = roi_df.iloc[0]
            st.success(
                f"Best Location for a ${budget} Budget: **{best['City']}**, **{best['State']}** with {int(best['Number of Panels'])} panels")

            # Download results
            st.download_button(
                label="📥 Download Results as CSV",
                data=roi_df.to_csv(index=False).encode('utf-8'),
                file_name=f'solar_roi_analysis_{region_selected}.csv',
                mime='text/csv',
            )
        else:
            st.error("No data retrieved. Check your API key or try fewer cities.")

else:
    st.error("Could not load cities CSV file. Please check the file path.")


# Add the calculate_solar_financials function
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

