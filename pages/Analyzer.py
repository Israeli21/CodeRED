# pages/Analyzer.py (Main Analyzer)
import streamlit as st
import pandas as pd
import plotly.express as px
from src.calculations import calculate_optimal_config

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
        <p style="color: #10b981; font-size: 1.3rem;">Find Your Optimal Renewable Energy Configuration</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.subheader("Define Your Constraints")
st.markdown("Specify any or all of the following parameters. Leave blank for AI recommendations.")

# Create 4 columns for the 4 main parameters
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("**Location**")
    location_input = st.selectbox(
        "Location",
        options=["Any", "West Texas", "Arizona Desert", "Southern Nevada", "Central California", "Great Plains"],
        label_visibility="collapsed",
        help="Select a location or 'Any' for recommendations"
    )
    location_specified = location_input != "Any"

with col2:
    st.markdown("**Budget ($)**")
    budget_input = st.number_input(
        "Budget",
        min_value=0,
        step=100000,
        value=0,
        label_visibility="collapsed",
        help="Enter a budget or leave as 0 for recommendations"
    )
    budget_specified = budget_input > 0

with col3:
    st.markdown("**Facility Type**")
    facility_type_input = st.selectbox(
        "Facility Type",
        options=["Any", "Solar Farm", "Wind Turbine", "Hydro Plant", "Hybrid (Solar+Wind)"],
        label_visibility="collapsed",
        help="Select a facility type or 'Any' for recommendations"
    )
    facility_type_specified = facility_type_input != "Any"

with col4:
    st.markdown("**Expected Annual Revenue ($)**")
    revenue_input = st.number_input(
        "Revenue",
        min_value=0,
        step=50000,
        value=0,
        label_visibility="collapsed",
        help="Enter target revenue or leave as 0 for recommendations"
    )
    revenue_specified = revenue_input > 0

st.divider()

col1, col2 = st.columns([1, 4])
with col1:
    optimize_button = st.button("Optimize", use_container_width=True, type="primary")

with col2:
    # Show which parameters are being used as filters
    specified = []
    if location_specified:
        specified.append(f"Location: {location_input}")
    if budget_specified:
        specified.append(f"Budget: ${budget_input:,}")
    if facility_type_specified:
        specified.append(f"Type: {facility_type_input}")
    if revenue_specified:
        specified.append(f"Revenue: ${revenue_input:,}")
    
    if specified:
        st.info(f"**Filtering by:** {' | '.join(specified)}")
    else:
        st.info("**No constraints set** - AI will recommend optimal configuration")

st.divider()

# Results Section
if optimize_button:
    with st.spinner("Optimizing renewable energy configuration..."):
        
        # Prepare input parameters
        params = {
            "location": location_input if location_specified else None,
            "budget": budget_input if budget_specified else None,
            "facility_type": facility_type_input if facility_type_specified else None,
            "revenue": revenue_input if revenue_specified else None
        }
        
        # Call optimization function from calculations module
        recommendations = calculate_optimal_config(params)
        
        # Display results
        st.subheader("Optimization Results")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Location",
                recommendations["location"],
                delta="92% Match" if not location_specified else "Specified"
            )
        
        with col2:
            st.metric(
                "Budget Required",
                f"${recommendations['budget']:,}",
                delta="Optimized" if not budget_specified else "Specified"
            )
        
        with col3:
            st.metric(
                "Facility Type",
                recommendations["facility_type"],
                delta="Recommended" if not facility_type_specified else "Specified"
            )
        
        with col4:
            st.metric(
                "Annual Revenue",
                f"${recommendations['revenue']:,}",
                delta="Projected" if not revenue_specified else "Specified"
            )
        
        st.divider()
        
        # Detailed Recommendation Table
        st.subheader("Configuration Details")
        
        config_details = {
            "Parameter": ["Location", "Budget", "Facility Type", "Expected Annual Revenue", "ROI Timeline", "CO2 Reduction/Year"],
            "Recommended Value": [
                recommendations["location"],
                f"${recommendations['budget']:,}",
                recommendations["facility_type"],
                f"${recommendations['revenue']:,}",
                recommendations.get("roi_timeline", "8-10 years"),
                recommendations.get("co2_reduction", "2,500 tons")
            ],
            "Confidence": ["92%", "88%", "95%", "85%", "89%", "91%"]
        }
        
        df_config = pd.DataFrame(config_details)
        st.dataframe(df_config, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Alternative Options
        st.subheader("Alternative Configurations")
        
        alternatives = recommendations.get("alternatives", [])
        df_alternatives = pd.DataFrame(alternatives)
        
        st.dataframe(
            df_alternatives,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Match Score": st.column_config.ProgressColumn(
                    "Match Score",
                    min_value=0,
                    max_value=100,
                ),
            }
        )
        
        st.divider()
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            fig_options = px.scatter(
                df_alternatives,
                x="Budget ($M)",
                y="Annual Revenue ($)",
                size="Match Score",
                color="Match Score",
                hover_name="Location",
                color_continuous_scale="Greens",
                title="Budget vs Revenue Options",
            )
            st.plotly_chart(fig_options, use_container_width=True)
        
        with col2:
            fig_match = px.bar(
                df_alternatives,
                x="Location",
                y="Match Score",
                color="Match Score",
                color_continuous_scale="Greens",
                title="Configuration Match Score"
            )
            st.plotly_chart(fig_match, use_container_width=True)
        
        st.divider()
        
        # Key Recommendations
        st.subheader("Key Recommendations")
        
        recs = recommendations.get("recommendations", [])
        for idx, rec in enumerate(recs, 1):
            st.info(f"{idx}. {rec}")

else:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center; padding: 3rem 0;">
                <p style="font-size: 1.3rem; color: #047857;">
                    Specify any combination of the 4 parameters above (or none for full recommendations) and click <b>Optimize</b> to find your ideal renewable energy configuration.
                </p>
                <br>
                <p style="font-size: 1rem; color: #059669;">
                    Examples:
                    <br>• Find best location for a $3M budget
                    <br>• Find best budget for Solar Farms in West Texas
                    <br>• Find best configuration for $500K annual revenue target
                    <br>• Get full AI recommendation (leave all blank)
                </p>
            </div>
        """, unsafe_allow_html=True)
