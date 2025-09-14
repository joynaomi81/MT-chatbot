import streamlit as st
import pandas as pd
import os

# App settings
st.set_page_config(page_title="Health Communication Data Curation", layout="wide")

# Initialize storage
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["ID", "Language", "Original Text", "English Translation", "Speaker Role", "Context", "Topic"])

# Sidebar menu
menu = ["Home", "Contribute Data", "View Data", "Download"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.title("🩺 Health Communication Data Curation")
    st.write("""
        This app collects examples of health communication in African languages.
        You can contribute doctor–patient conversations, health campaign messages, or translations.
        The goal is to build a dataset for discourse analysis and AI healthcare applications.
    """)

elif choice == "Contribute Data":
    st.title("✍️ Contribute Health Communication Data")

    with st.form("curation_form"):
        lang = st.selectbox("Language", ["Yoruba", "Swahili", "Hausa", "Igbo", "Zulu", "Other"])
        original = st.text_area("Original Text (local language)")
        translation = st.text_area("English Translation")
        role = st.selectbox("Speaker Role", ["Doctor", "Patient", "Campaign Voice", "Other"])
        context = st.selectbox("Context", ["Clinic", "Hospital", "Radio", "Poster", "Conversation", "Other"])
        topic = st.text_input("Topic (e.g., Malaria, HIV, Maternal Health)")
        submitted = st.form_submit_button("Save Entry")

        if submitted:
            if original and translation:
                new_entry = {
                    "ID": len(st.session_state.data) + 1,
                    "Language": lang,
                    "Original Text": original,
                    "English Translation": translation,
                    "Speaker Role": role,
                    "Context": context,
                    "Topic": topic
                }
                st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_entry])], ignore_index=True)
                st.success("✅ Entry saved!")
            else:
                st.error("Please provide both the original text and translation.")

elif choice == "View Data":
    st.title("📊 Collected Data")
    if not st.session_state.data.empty:
        st.dataframe(st.session_state.data, use_container_width=True)
    else:
        st.info("No data collected yet. Go to 'Contribute Data' to add.")

elif choice == "Download":
    st.title("⬇️ Download Dataset")
    if not st.session_state.data.empty:
        csv = st.session_state.data.to_csv(index=False)
        st.download_button("Download as CSV", csv, file_name="health_communication_dataset.csv", mime="text/csv")
    else:
        st.info("No data to download yet.")
