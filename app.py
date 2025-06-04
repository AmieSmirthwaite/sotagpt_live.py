import streamlit as st
import openai
import requests

# Set your OpenAI API key (you can use secrets in Streamlit Cloud or locally)
openai.api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI()

st.set_page_config(page_title="SotaGPT with Real Clinical Data", layout="centered")

st.title("SotaGPT: Real Clinical Evidence Summarizer")

st.markdown("Enter a medical device or product type to retrieve recent evidence and generate a summary.")

# User Input
device_query = st.text_input("Device Type or Product Name", placeholder="e.g., radiotherapy bead")

# Helper function to query PubMed API
def fetch_pubmed_abstracts(query, max_results=5):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }
    response = requests.get(base_url, params=params)
    ids = response.json().get("esearchresult", {}).get("idlist", [])

    abstracts = []
    if ids:
        id_string = ",".join(ids)
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        fetch_params = {
            "db": "pubmed",
            "id": id_string,
            "retmode": "text",
            "rettype": "abstract"
        }
        fetch_response = requests.get(fetch_url, params=fetch_params)
        abstracts = fetch_response.text.split("\n\n")
    return abstracts

# Button to Trigger Retrieval and Summary
if st.button("Generate Evidence-Based SOTA Report"):
    if device_query:
        with st.spinner("Fetching clinical evidence and generating summary..."):
            abstracts = fetch_pubmed_abstracts(device_query)
            joined_abstracts = "\n".join(abstracts[:3])

            prompt = (
                f"You are a clinical evidence analyst. Based on the following real abstracts about '{device_query}', "
                "summarize the state of the art in terms of: \n"
                "1. Therapeutic alternatives\n"
                "2. Clinical outcome parameters and acceptance criteria\n"
                "3. Safety and performance requirements\n"
                "4. Applicable guidelines or regulatory frameworks\n"
                "Use clear bullet points in your summary.\n\n"
                f"Abstracts:\n{joined_abstracts}"
            )

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You summarize real-world clinical evidence for regulatory context."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.6
                )
                result = response.choices[0].message.content
                st.markdown("---")
                st.markdown("### Generated Evidence-Based SOTA Report")
                st.markdown(result)
            except openai.RateLimitError:
                st.error("Rate limit exceeded. Please try again later.")
    else:
        st.warning("Please enter a device type or name first.")
