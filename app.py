import streamlit as st
import openai

# Set your OpenAI API key (you can use secrets in Streamlit Cloud for safety)
openai.api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI()

st.set_page_config(page_title="SotaGPT Live: Real-Time SOTA Generator", layout="centered")

st.title("SotaGPT Live: Real-Time SOTA Summary Generator")

st.markdown("Enter a medical device or product type to generate a plausible SOTA report using AI and current clinical knowledge.")

# User Input
device_query = st.text_input("Device Type or Product Name", placeholder="e.g., radiotherapy bead")

if st.button("Generate Live SOTA Report"):
    if device_query:
        prompt = (
            f"You are a clinical evidence analyst. Based on the device: '{device_query}', "
            "provide a plausible summary of:\n"
            "1. Therapeutic alternatives\n"
            "2. Clinical outcome parameters and typical acceptance criteria\n"
            "3. Safety and performance requirements\n"
            "4. Guidelines or regulatory references (fictio
