import streamlit as st
import openai

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
            "4. Guidelines or regulatory references (fictional but plausible)\n"
            "Present results in clear bullet points for each section."
        )

        with st.spinner("Generating plausible SOTA summary..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You summarize clinical device evidence."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            result = response.choices[0].message.content
            st.markdown("---")
            st.markdown("### Generated SOTA Report")
            st.markdown(result)
    else:
        st.warning("Please enter a device type or name first.")
