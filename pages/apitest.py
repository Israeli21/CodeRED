import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

#Load .env file
load_dotenv()

#Get API key
api_key = os.getenv("OPENAI_API_KEY")

#Initialize OpenAI client
client = OpenAI(api_key=api_key)

st.title("🔍 OpenAI API Connection Test")

#Input box for a quick prompt
prompt = st.text_input("Enter a prompt:", "Say hello!")

if st.button("Send to OpenAI"):
    with st.spinner("Contacting OpenAI..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Fast, cheap model for testing
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            st.success("✅ Connection successful!")
            st.write("Response:")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"❌ Error: {e}")