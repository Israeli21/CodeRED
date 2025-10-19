import streamlit as st
import pandas as pd
import plotly.express as px
import os
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
    
    .stMetric {
        background-color: #d1fae5;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #10b981;
    }
    
    .stButton > button {
        background-color: #10b981;
        color: white;
        font-size: 1.1rem;
    }
    
    .stButton > button:hover {
        background-color: #059669;
    }
    
    /* Make filter labels bigger */
    .stSelectbox label, .stNumberInput label {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }
    
    /* Make expander content bigger */
    .streamlit-expanderHeader {
        font-size: 1.3rem !important;
        padding: 1.5rem !important;
    }
    
    .streamlit-expanderContent p {
        font-size: 1.1rem !important;
        line-height: 1.8 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 3rem; margin: 0; font-weight: 900; color: #047857;">Energy Optimizer</h1>
        <p style="color: #10b981; font-size: 1.3rem;">Calculate Revenue for Your Renewable Energy Project</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Load wind turbine data
@st.cache_data
def load_wind_data():
    csv_path = "renewable_energies/wind/optimal_wind_turbine_locations.csv"
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        st.error(f"Wind data file not found at {csv_path}")
        return None

@st.cache_data(show_spinner="Loading location names...")
def get_location_name(lat, lon):
    try:
        geocoder = Nominatim(user_agent="renewweb_analyzer")
        location = geocoder.reverse(f"{lat}, {lon}", language='en', timeout=10)
        if location and location.raw.get('address'):
            address = location.raw['address']
            state = address.get('state', None)
            country = address.get('country', None)

            if state:
                return state, True  # Valid location with state
            elif country:
                return country, True  # At least a country found
        return None, False  # Invalid location
    except Exception:
        return None, False  # On error

def get_valid_locations(df_sorted, count=5):
    valid_rows = []
    for idx, row in df_sorted.iterrows():
        location_name, is_valid = get_location_name(row['lat'], row['lon'])
        if is_valid:
            row['Location'] = location_name
            valid_rows.append(row)
        if len(valid_rows) >= count:
            break
    return pd.DataFrame(valid_rows)


st.subheader("Wind Turbine Configuration")
    
col1, col2 = st.columns(2)
    
with col1:
    cost_per_unit = st.number_input(
        "Cost per Wind Turbine ($M)",
        min_value=1.5,
        max_value=10.0,
        value=1.5,
        step=0.5,
        help="Select the construction cost per wind turbine in millions"
    )
    
with col2:
    num_units = st.number_input(
        "Number of Wind Turbines",
        min_value=1,
        max_value=1000,
        value=10,
        step=1,
        help="How many wind turbines do you want to build?"
    )
    
efficiency_value = st.slider(
    "Turbine Efficiency (%)",
    min_value=10,
    max_value=100,
    value=50,
    step=1,
    help="Select the efficiency rating of the turbines (10-100%)"
)
efficiency = f"{efficiency_value}%"
    
st.divider()
    
if st.button("GENERATE REVENUE CALCULATIONS", use_container_width=True, type="primary"):
    wind_df = load_wind_data()
    st.session_state.renewable_source = "Wind"
    st.session_state.cost_per_unit = cost_per_unit
    st.session_state.num_units = num_units
    st.session_state.efficiency = efficiency
    st.session_state.wind_df = wind_df
    st.session_state.show_results = True

# Display results if generated
if "show_results" in st.session_state and st.session_state.show_results:
    wind_df = st.session_state.wind_df
    if wind_df is not None:
        st.divider()
        st.subheader("Revenue Analysis Results")
        
        # Extract efficiency as decimal
        efficiency_num = int(st.session_state.efficiency.replace('%', '')) / 100
        capacity_factor = efficiency_num
        
        # Constants for calculations
        turbine_capacity_mw = 2.0  # MW per turbine
        annual_hours = 8760
        energy_price = 0.05  # $/kWh
        om_cost_per_mw_year = 45000  # $/MW/year
        
        
        
        
        def calculate_wind_metrics(row, num_turbines, capacity_factor, cost_per_unit_millions):
            total_capacity_mw = float(num_turbines) * float(turbine_capacity_mw)

            # Use wind quality as a multiplier — you can choose either:
    
            # Option A: Based on mean wind speed (cubed is more realistic for turbines)
            wind_multiplier = (float(row['mean_wind_speed']) / 8.0) ** 3  # Normalize to 8 m/s

            # Option B: Based on power_potential (already in a relevant scale)
            # wind_multiplier = float(row['power_potential']) / 600.0  # Normalize around median

            annual_energy_kwh = (
                float(num_turbines)
                * float(turbine_capacity_mw)
                * float(annual_hours)
                * float(capacity_factor)
                * wind_multiplier
                * 1000.0
            )

            annual_revenue = float(annual_energy_kwh) * float(energy_price)
            om_cost = float(total_capacity_mw) * float(om_cost_per_mw_year)
            annual_profit = annual_revenue - om_cost
            total_cost = float(cost_per_unit_millions) * 1e6 * float(num_turbines)
    
            roi_percent = (annual_profit / total_cost * 100.0) if total_cost > 0 else 0
            payback_years = (total_cost / annual_profit) if annual_profit > 0 else float('inf')

            return {
             'Annual Energy (MWh)': annual_energy_kwh / 1e6,
                'Annual Revenue ($M)': annual_revenue / 1e6,
                'Annual Profit ($M)': annual_profit / 1e6,
                'ROI (%)': roi_percent,
                'Payback (years)': payback_years
            }


        # Calculate metrics for all locations (without location names initially)
        results = []
        for idx, row in wind_df.iterrows():
            metrics = calculate_wind_metrics(row, st.session_state.num_units, capacity_factor, st.session_state.cost_per_unit)
            result_row = {
                'Location': f"({row['lat']:.2f}, {row['lon']:.2f})",  # Placeholder
                'lat': row['lat'],
                'lon': row['lon'],
                **metrics
            }
            results.append(result_row)
        
        df_results = pd.DataFrame(results)
        
        # Sort by Annual Revenue for initial display metrics
        df_top5_initial = df_results.nlargest(5, 'Annual Revenue ($M)').reset_index(drop=True)
        
        # Display metrics vertically (stacked)
        st.metric("Total Investment", f"${st.session_state.cost_per_unit * st.session_state.num_units:.1f}M")
        st.metric("Top Location Revenue", f"${df_top5_initial.iloc[0]['Annual Revenue ($M)']:.1f}M/yr")
        st.metric("Best ROI", f"{df_top5_initial.iloc[0]['ROI (%)']:.1f}%")
        st.metric("Fastest Payback", f"{df_top5_initial.iloc[0]['Payback (years)']:.1f} yrs")
        st.metric("Source", st.session_state.renewable_source)
        
        st.divider()
        
        # MOVED OUTSIDE: Sorting and filtering options - now updates automatically
        sort_by = st.selectbox(
            "Top 5 locations by",
            options=[
                "Revenue",
                "Profit",
                "Energy",
                "Payback Period",
                "ROI"
            ],
            help="Select the metric to sort locations by"
        )
        
        # Map selection to column name and whether to use nsmallest (for lower is better)
        sort_mapping = {
            "Revenue": ("Annual Revenue ($M)", False),
            "Profit": ("Annual Profit ($M)", False),
            "Energy": ("Annual Energy (MWh)", False),
            "Payback Period": ("Payback (years)", True),  # Lower is better
            "ROI": ("ROI (%)", False)
        }
        
        sort_column, use_smallest = sort_mapping[sort_by]
        
        # Range filtering based on selected metric
        st.subheader(f"Filter by {sort_by} Range (Optional)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            min_val = st.number_input(f"Minimum {sort_by}", value=None, placeholder="Leave empty for no minimum")
        
        with col2:
            max_val = st.number_input(f"Maximum {sort_by}", value=None, placeholder="Leave empty for no maximum")
        
        st.divider()
        
        # Apply range filter if specified
        df_filtered = df_results.copy()
        
        if min_val is not None:
            df_filtered = df_filtered[df_filtered[sort_column] >= min_val]
        if max_val is not None:
            df_filtered = df_filtered[df_filtered[sort_column] <= max_val]
        
        # Sort and get top 5 and bottom 5
        if use_smallest:
            df_top5 = df_filtered.nsmallest(5, sort_column).reset_index(drop=True)
            df_bottom5 = df_filtered.nlargest(5, sort_column).reset_index(drop=True)
        else:
            # Pre-sort
            df_sorted_top = df_filtered.sort_values(by=sort_column, ascending=use_smallest).reset_index(drop=True)
            df_sorted_bottom = df_filtered.sort_values(by=sort_column, ascending=not use_smallest).reset_index(drop=True)

            # Get only valid location rows (up to 5)
            df_top5 = get_valid_locations(df_sorted_top, count=5)
            df_bottom5 = get_valid_locations(df_sorted_bottom, count=5)
        
        # NOW get location names only for the top 5 and bottom 5 using EXACT coordinates
        for idx in df_top5.index:
            exact_lat = df_top5.at[idx, 'lat']
            exact_lon = df_top5.at[idx, 'lon']
            location_name, _ = get_location_name(exact_lat, exact_lon)
            df_top5.at[idx, 'Location'] = location_name if location_name else f"({exact_lat:.2f}, {exact_lon:.2f})"

        
        for idx in df_bottom5.index:
            exact_lat = df_bottom5.at[idx, 'lat']
            exact_lon = df_bottom5.at[idx, 'lon']
            location_name, _ = get_location_name(exact_lat, exact_lon)
            df_bottom5.at[idx, 'Location'] = location_name if location_name else f"({exact_lat:.2f}, {exact_lon:.2f})"
        
        if len(df_top5) == 0:
            st.warning("No locations found for the selected range")
        else:
            st.divider()
            
            # Display TOP 5 results
            st.subheader(f"Top 5 Locations by {sort_by} ({len(df_top5)} results)")
            
            for idx, row in df_top5.iterrows():
                with st.expander(f"{idx+1}. {row['Location']} - ${row['Annual Revenue ($M)']:.5f}M Revenue / {row['ROI (%)']:.5f}% ROI"):
                    st.markdown(f"<p style='font-size: 1.15rem;'><strong>Annual Energy:</strong> {row['Annual Energy (MWh)']:,.5f} MWh/yr</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.15rem;'><strong>Annual Revenue:</strong> ${row['Annual Revenue ($M)']:.5f}M</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.15rem;'><strong>Annual Profit:</strong> ${row['Annual Profit ($M)']:.5f}M</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.15rem;'><strong>ROI:</strong> {row['ROI (%)']:.5f}%</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.15rem;'><strong>Payback Period:</strong> {row['Payback (years)']:.5f} years</p>", unsafe_allow_html=True)
                    
                    if st.button("VIEW ON MAP", key=f"map_top_{idx}", use_container_width=True):
                        # Store full precision coordinates
                        st.session_state.selected_location = f"{row['lat']},{row['lon']}"
                        st.session_state.selected_lat = float(row['lat'])
                        st.session_state.selected_lon = float(row['lon'])
                        st.session_state.location_name = row['Location']
                        st.session_state.latitude = float(row['lat'])
                        st.session_state.longitude = float(row['lon'])
                        st.session_state.show_map = True
                        st.switch_page("pages/SiteMap.py")
            
            st.divider()
            
            # Display BOTTOM 5 results
            st.subheader(f"Bottom 5 Locations by {sort_by} ({len(df_bottom5)} results)")
            
            for idx, row in df_bottom5.iterrows():
                with st.expander(f"{idx+1}. {row['Location']} - ${row['Annual Revenue ($M)']:.5f}M Revenue / {row['ROI (%)']:.5f}% ROI"):
                    st.markdown(f"<p style='font-size: 1.15rem;'><strong>Annual Energy:</strong> {row['Annual Energy (MWh)']:,.5f} MWh/yr</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.15rem;'><strong>Annual Revenue:</strong> ${row['Annual Revenue ($M)']:.5f}M</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.15rem;'><strong>Annual Profit:</strong> ${row['Annual Profit ($M)']:.5f}M</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.15rem;'><strong>ROI:</strong> {row['ROI (%)']:.5f}%</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.15rem;'><strong>Payback Period:</strong> {row['Payback (years)']:.5f} years</p>", unsafe_allow_html=True)
                    
                    if st.button("VIEW ON MAP", key=f"map_bottom_{idx}", use_container_width=True):
                        # Store full precision coordinates
                        st.session_state.selected_location = f"{row['lat']},{row['lon']}"
                        st.session_state.selected_lat = float(row['lat'])
                        st.session_state.selected_lon = float(row['lon'])
                        st.session_state.location_name = row['Location']
                        st.session_state.latitude = float(row['lat'])
                        st.session_state.longitude = float(row['lon'])
                        st.session_state.show_map = True
                        st.switch_page("pages/SiteMap.py")
            
            st.divider()
            
            # Visualization with TOP 5 only
            st.subheader(f"Top 5 {sort_by} Comparison by Location")
            
            fig = px.bar(
                df_top5,
                x="Location",
                y=sort_column,
                color="ROI (%)",
                color_continuous_scale="Greens",
                title=f"Top 5 by {sort_by}",
                labels={sort_column: sort_column},
                height=600  # Increased from default ~450 to 600
            )
            
            # Make bars thicker and improve layout
            fig.update_traces(width=0.6)
            fig.update_layout(
                xaxis_tickangle=-45,
                margin=dict(b=100)
            )
            
            st.plotly_chart(fig, use_container_width=True)