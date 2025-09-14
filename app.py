import streamlit as st
import pandas as pd
import os

# File to store submissions
DATA_FILE = "taboo_curation.csv"

# Load existing data if file exists
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Language", "Forbidden_Practice", "Meaning", "Curator"])

# Sidebar navigation
st.sidebar.title("📑 Cultural Taboo Curation")
page = st.sidebar.radio("Navigate", ["Submit Entry", "Review Data", "Download Data"])

st.title("🗣️ Yoruba & Igbo Cultural Taboo Curation Platform")
st.write("Contribute knowledge of cultural taboos and their meanings in Yoruba and Igbo communities.")

if page == "Submit Entry":
    st.subheader("✍️ Submit a Cultural Taboo")
    
    language = st.selectbox("Language", ["Yoruba", "Igbo"])
    forbidden_practice = st.text_area("Describe the forbidden practice (e.g., 'Pregnant woman walking in the sun')")
    meaning = st.text_area("Meaning or cultural explanation in English")
    curator = st.text_input("Your Name (optional)")

    if st.button("Submit"):
        if forbidden_practice.strip() == "":
            st.warning("Forbidden practice cannot be empty.")
        else:
            new_row = pd.DataFrame({
                "Language": [language],
                "Forbidden_Practice": [forbidden_practice],
                "Meaning": [meaning],
                "Curator": [curator]
            })
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ Entry submitted successfully!")

elif page == "Review Data":
    st.subheader("🔍 Review Submitted Taboos")
    if df.empty:
        st.info("No entries available yet.")
    else:
        st.dataframe(df)

elif page == "Download Data":
    st.subheader("📥 Download Curated Dataset")
    if df.empty:
        st.info("No data to download yet.")
    else:
        st.download_button(
            label="Download as CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="cultural_taboo_curation.csv",
            mime="text/csv"
        )
        st.download_button(
            label="Download as JSON",
            data=df.to_json(orient="records", force_ascii=False, indent=2),
            file_name="cultural_taboo_curation.json",
            mime="application/json"
        )
