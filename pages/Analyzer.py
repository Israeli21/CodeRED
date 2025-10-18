import streamlit as st
import pandas as pd
import plotly.express as px

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
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 3rem; margin: 0; font-weight: 900; color: #047857;">Energy Optimizer</h1>
        <p style="color: #10b981; font-size: 1.3rem;">Calculate Revenue for Your Renewable Energy Project</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Step 1: Select Renewable Energy Source
st.subheader("Step 1: Select Renewable Energy Source")

renewable_source = st.selectbox(
    "Choose your renewable energy source:",
    options=["Select an option", "Wind"],
    index=0,
    help="Select the type of renewable energy you want to build"
)

st.divider()

# Step 2: Dynamic inputs based on source selection
if renewable_source == "Select an option":
    st.info("Please select a renewable energy source to continue")

elif renewable_source == "Wind":
    st.subheader("Step 2: Wind Turbine Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cost per unit with +/- buttons
        cost_per_unit = st.number_input(
            "Cost per Wind Turbine ($M)",
            min_value=1.5,
            max_value=10.0,
            value=1.5,
            step=0.5,
            help="Select the construction cost per wind turbine in millions"
        )
    
    with col2:
        # Number of units
        num_units = st.number_input(
            "Number of Wind Turbines",
            min_value=1,
            max_value=1000,
            value=10,
            step=1,
            help="How many wind turbines do you want to build?"
        )
    
    # Efficiency slider (full width below)
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
    
    # Generate button
    if st.button("GENERATE REVENUE CALCULATIONS", use_container_width=True, type="primary"):
        
        # Store parameters in session state
        st.session_state.renewable_source = "Wind"
        st.session_state.cost_per_unit = cost_per_unit
        st.session_state.num_units = num_units
        st.session_state.efficiency = efficiency
        st.session_state.show_results = True



# Display results if generated
if "show_results" in st.session_state and st.session_state.show_results:
    
    st.divider()
    st.subheader("Revenue Analysis Results")
    
    # Sample data for top 5 locations
    efficiency_num = int(st.session_state.efficiency.replace('%', ''))  # Remove % and convert to int
    base_revenue = st.session_state.num_units * st.session_state.cost_per_unit * 0.25 * (efficiency_num / 100)
    
    results_data = {
        "Location": ["West Texas", "Arizona Desert", "Southern Nevada", "Central California", "Great Plains"],
        "Annual Energy (MWh)": [850000, 820000, 780000, 750000, 620000],
        "Annual Revenue ($M)": [2.5, 2.4, 2.3, 2.2, 1.8],
        "Annual Profit ($M)": [1.8, 1.7, 1.6, 1.5, 1.1],
        "ROI (%)": [45, 42, 40, 38, 35],
        "Payback (years)": [2.2, 2.4, 2.5, 2.6, 2.8]
    }
    
    df_results = pd.DataFrame(results_data)
    
    # Display metrics vertically (stacked)
    st.metric("Total Investment", f"${st.session_state.cost_per_unit * st.session_state.num_units:.1f}M")
    st.metric("Top Location Revenue", f"${df_results.iloc[0]['Annual Revenue ($M)']:.1f}M/yr")
    st.metric("Best ROI", f"{df_results.iloc[0]['ROI (%)']:.0f}%")
    st.metric("Fastest Payback", f"{df_results.iloc[0]['Payback (years)']:.1f} yrs")
    st.metric("Source", st.session_state.renewable_source)
    
    st.divider()
    
    # Display results in collapsible format with bigger expanders
    st.subheader("Top 5 Locations by Revenue")
    
    # Add CSS to make expanders bigger
    st.markdown("""
        <style>
        .streamlit-expanderHeader {
            font-size: 1.3rem !important;
            padding: 1.5rem !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    for idx, row in df_results.iterrows():
        with st.expander(f"{idx+1}. {row['Location']} - ${row['Annual Revenue ($M)']:.1f}M Revenue / {row['ROI (%)']:.0f}% ROI"):
            st.write(f"**Annual Energy:** {row['Annual Energy (MWh)']:,.0f} MWh/yr")
            st.write(f"**Annual Revenue:** ${row['Annual Revenue ($M)']:.1f}M")
            st.write(f"**Annual Profit:** ${row['Annual Profit ($M)']:.1f}M")
            st.write(f"**ROI:** {row['ROI (%)']:.0f}%")
            st.write(f"**Payback Period:** {row['Payback (years)']:.1f} years")
            
            if st.button("VIEW ON MAP", key=f"map_{idx}", use_container_width=True):
                st.session_state.selected_location = row['Location']
                st.session_state.show_map = True
                st.switch_page("pages/SiteMap.py")
    
    st.divider()
    
    # Visualization
    st.subheader("Revenue Comparison by Location")
    
    fig = px.bar(
        df_results,
        x="Location",
        y="Annual Revenue ($M)",
        color="ROI (%)",
        color_continuous_scale="Greens",
        title="Annual Revenue and ROI by Location",
        labels={"Annual Revenue ($M)": "Revenue ($M)"}
    )
    st.plotly_chart(fig, use_container_width=True)