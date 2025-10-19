import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Custom styling to match your other pages
st.markdown("""
    <style>
    .main {
        padding: 1.5rem;
        background-color: #f0fdf4;
    }
    
    h1, h2, h3 {
        color: #047857;
    }
    
    .stTextInput > div > input {
        font-size: 1.1rem;
    }
    
    .stButton > button {
        background-color: #10b981;
        color: white;
        font-size: 1.1rem;
        padding: 0.6rem 1rem;
    }
    
    .stButton > button:hover {
        background-color: #059669;
    }
    
    .chat-response {
        background-color: #ecfdf5;
        padding: 1rem;
        border-left: 5px solid #10b981;
        border-radius: 0.5rem;
        margin-top: 1rem;
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <div style="font-size: 6rem; color: #10b981;">🤖</div>
    <h1 style="font-size: 3rem; font-weight: 900; color: #047857; margin-top: 0.5rem;">Smart Location Assistant</h1>
    <p style="color: #10b981; font-size: 1.2rem;">
        Ask questions about energy locations, environments, renewable tech, or regulations.
    </p>
</div>
""", unsafe_allow_html=True)



st.divider()

# Prompt input
st.markdown("Ask me anything")
user_prompt = st.text_input("For example: *What are the environmental risks in Nuevo León?*", placeholder="Type your question here...")

# Button to send query
if st.button("Ask the Assistant"):
    if not user_prompt.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Contacting the assistant..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",  # Use gpt-4o for better answers
                    messages=[
                        {"role": "system", "content": "You are an expert assistant helping users evaluate renewable energy opportunities. Answer questions related to location, climate, energy infrastructure, regulations, or environmental impact in a clear and helpful way."},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                message = response.choices[0].message.content
                st.markdown(f"<div class='chat-response'>{message}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error: {e}")
