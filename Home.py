import streamlit as st

# ================== Custom CSS ===================
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
        color: var(--dark-green);
    }

    .stButton > button {
        background-color: var(--primary-green);
        color: white;
        font-size: 1.1rem;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
    }

    .stButton > button:hover {
        background-color: #059669;
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        color: var(--dark-green);
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1.5rem;
        color: var(--primary-green);
        font-weight: 600;
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--dark-green);
        margin-top: 3rem;
        margin-bottom: 1rem;
    }

    .step {
        font-size: 1.1rem;
        margin-bottom: 0.75rem;
    }

    .audience-box {
        background-color: var(--light-green);
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
        border-left: 5px solid var(--primary-green);
    }

    .audience-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--dark-green);
        margin-bottom: 0.5rem;
    }

    .audience-desc {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #333;
    }

    .cta {
        text-align: center;
        margin-top: 3rem;
    }

    .footer {
        font-size: 1rem;
        color: #555;
        text-align: center;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ================== Hero Section ===================
st.markdown("""
<div style="text-align: center; padding: 3rem 0;">
    <div class="hero-title">RenewWeb</div>
    <div class="hero-subtitle">~Where renewables thrive~</div>
</div>
""", unsafe_allow_html=True)

# ================== About Section ===================
st.markdown("""
<div class="section-title">What is RenewWeb?</div>

<p style="font-size: 1.1rem; line-height: 1.8;">
    <strong>RenewWeb</strong> is an AI-powered platform that empowers you to make smarter decisions 
    about renewable energy site development. Whether you're an <strong>investor</strong>, an <strong>environmentalist</strong>, 
    or simply <strong>curious</strong> about the clean energy future — we provide tailored recommendations 
    for optimal renewable energy projects across the United States and beyond.
</p>
""", unsafe_allow_html=True)

# ================== How It Works ===================
st.markdown("""
<div class="section-title">How It Works</div>

<div class="step">1. <strong>Select your energy type</strong> – Wind, solar, or more to come</div>
<div class="step">2. <strong>Configure your inputs</strong> – Budget, efficiency, number of units, or target revenue</div>
<div class="step">3. <strong>Run the optimizer</strong> – Our ML model uses environmental, financial, and location data</div>
<div class="step">4. <strong>Get intelligent recommendations</strong> – See revenue, ROI, and payback for each site</div>
<div class="step">5. <strong>Visualize on the map</strong> – Explore location impacts and future potential</div>
""", unsafe_allow_html=True)

# ================== Use Cases ===================
st.markdown("""
<div class="section-title">Who Is This For?</div>

<div class="audience-box">
    <div class="audience-title">For Investors</div>
    <div class="audience-desc">
        Evaluate where to get the highest return on clean energy investments.
        Compare ROI, annual revenue, and payback time across regions — all backed by real-world data.
    </div>
</div>

<div class="audience-box">
    <div class="audience-title">For Curious Minds & Environmentalists</div>
    <div class="audience-desc">
        Explore how environmental factors affect energy production. 
        Understand how location, efficiency, and technology shape the future of sustainability.
    </div>
</div>
""", unsafe_allow_html=True)

# Custom CSS for buttons
st.markdown("""
    <style>
    .stButton > button {
        background-color: #10b981;
        color: white;
        font-size: 1.5rem;           /* Bigger text */
        font-weight: 600;
        padding: 1.2rem 2rem;        /* Bigger button height */
        border-radius: 0.7rem;
        width: 100%;
        margin-top: 1rem;
        transition: background-color 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #059669;
    }
    </style>
""", unsafe_allow_html=True)



# Use columns with width ratios to center the button
col1, col2, col3 = st.columns([2, 1, 2])  # Center column for button

with col2:
    if st.button("Wind", use_container_width=True, key="wind_button"):
        st.switch_page("pages/Wind.py")

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)  # spacer

    if st.button("Solar", use_container_width=True, key="solar_button"):
        st.switch_page("pages/Solar.py")



# ================== Footer ===================
st.markdown("""
<div class="footer">
    Built with purpose, powered by data — Let's make renewable energy smarter.
</div>
""", unsafe_allow_html=True)
