import streamlit as st

# Custom styling - Pastel Green Color Palette
st.markdown("""
    <style>
    * {
        --primary-green: #10b981;
        --pastel-green: #d1fae5;
        --light-green: #ecfdf5;
        --dark-green: #047857;
    }
    
    .main {
        padding: 2rem;
        background-color: #f0fdf4;
    }
    
    h1, h2, h3 {
        color: #047857;
        font-size: 2.5rem;
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
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
    }
    
    .stButton > button:hover {
        background-color: #059669;
    }
    
    .stRadio > label {
        font-size: 1.1rem;
    }
    
    .stSelectbox > label {
        font-size: 1.1rem;
    }
    
    .stNumberInput > label {
        font-size: 1.1rem;
    }
    
    .stSlider > label {
        font-size: 1.1rem;
    }
    
    .stSubheader {
        color: #047857;
        font-size: 1.8rem;
    }
    
    .stMarkdown {
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <h1 style="font-size: 4rem; margin: 0; font-weight: 900; color: #047857;">RenewWeb</h1>
        <h2 style="font-size: 2.5rem; color: #10b981; margin: 1rem 0; font-weight: 600;">"Where renewables thrive"</h2>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.markdown("""
    ### Welcome to RenewWeb
    
    **An AI-powered platform for optimizing renewable energy investments.**
    
    ---
    
    #### How it works:
    1. **Choose your parameters** - Specify any combination of Location, Budget, Facility Type, or Revenue
    2. **Set your constraints** - Input the values that matter to your investment
    3. **Click Optimize** - Our ML model analyzes and recommends optimal configurations
    4. **Get recommendations** - Receive optimal locations, budgets, facility types, and revenue projections
    
    #### Features:
    - Historical weather data integration (via Meteomatics API)
    - ML-powered multi-parameter optimization
    - Flexible query system (specify any or all parameters)
    - Interactive location mapping
    - ROI and cost projections
    - Alternative configuration suggestions
    
    ---
""")

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Get Started", use_container_width=True, type="primary"):
        st.switch_page("pages/Analyzer.py")

st.markdown("""
    ---
    
    **Ready to optimize your renewable energy investment?**
    
    Click the button above to begin your analysis!
""")
