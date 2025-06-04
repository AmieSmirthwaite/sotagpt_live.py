import streamlit as st
import openai

st.set_page_config(page_title="SotaGPT Live: Real-Time SOTA Generator", layout="centered")

st.title("SotaGPT Live: Real-Time SOTA Summary Generator")

st.markdown("Enter a medical device or product type to generate a plausible SOTA report using AI and current clinical knowledge.")

# User Input
device_query = st.text_input("Device Type or Product Name", placeholder="e.g., radiotherapy bead")

if st.button("Generate Live SOTA Report"):
    if device_query:
        # AI prompt to generate plausible conclusions
        prompt = (
            f"You are a clinical evidence analyst. Based on the device: '{device_query}', "
