import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# -----------------------------
# Config (using secrets.toml)
# -----------------------------
ADMIN_PASSWORD = st.secrets["admin"]["password"]
DATA_FILE = "user_progress.json"


# -----------------------------
# Helpers for Saving/Loading
# -----------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# -----------------------------
# Metadata Page
# -----------------------------
def metadata_page(username):
    st.subheader("📝 User Metadata")

    all_data = load_data()
    user_data = all_data.get(username, {})
    metadata = user_data.get("metadata", {})

    name = st.text_input("Full Name", metadata.get("name", ""))
    sex = st.selectbox(
        "Sex", ["Male", "Female", "Other"],
        index=["Male", "Female", "Other"].index(metadata.get("sex", "Male"))
    )
    age = st.number_input("Age", min_value=10, max_value=120, value=metadata.get("age", 18))
    gmail = st.text_input("Gmail", metadata.get("gmail", ""))
    country = st.text_input("Country", metadata.get("country", ""))

    if st.button("Save Metadata"):
        user_data["metadata"] = {
            "name": name.strip(),
            "sex": sex,
            "age": age,
            "gmail": gmail.strip(),
            "country": country.strip()
        }
        all_data[username] = user_data
        save_data(all_data)
        st.success("✅ Metadata saved successfully!")

        # Auto move to Curation page
        st.session_state.page = "Curate"
        st.rerun()


# -----------------------------
# Curation Page (No user data shown)
# -----------------------------
def curation_page(username):
    st.subheader("📦 Taboo Curation")

    all_data = load_data()
    user_data = all_data.get(username, {})

    if "curations" not in user_data:
        user_data["curations"] = {}

    curated_count = len(user_data["curations"])

    with st.form("curation_form"):
        taboo = st.text_input("Enter Taboo")
        meaning = st.text_area("Enter Meaning of the Taboo")
        label = st.text_input("Enter Label (e.g., taboo)")

        submitted = st.form_submit_button("Save")
        if submitted:
            if taboo and meaning and label:
                user_data["curations"][str(curated_count + 1)] = {
                    "taboo": taboo.strip(),
                    "meaning": meaning.strip(),
                    "label": label.strip(),
                    "timestamp": datetime.now().isoformat()
                }
                all_data[username] = user_data
                save_data(all_data)
                st.success("✅ Entry saved successfully!")
                st.rerun()
            else:
                st.error("⚠️ Please fill in all fields before saving.")


# -----------------------------
# Admin Page
# -----------------------------
def admin_page():
    st.subheader("🛡️ Admin Dashboard")

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        password = st.text_input("Enter Admin Password", type="password")
        if st.button("Login as Admin"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.success("✅ Welcome, Admin!")
                st.rerun()
            else:
                st.error("❌ Incorrect password.")
        return

    data = load_data()
    if not data:
        st.info("No user data yet.")
        return

    progress_data = []
    metadata_rows = []
    curation_rows = []

    for user, details in data.items():
        curations = details.get("curations", {})
        metadata = details.get("metadata", {})

        progress_data.append({
            "User": user,
            "Completed": len(curations),
        })

        metadata_rows.append({
            "User": user,
            "Name": metadata.get("name", ""),
            "Sex": metadata.get("sex", ""),
            "Age": metadata.get("age", ""),
            "Gmail": metadata.get("gmail", ""),
            "Country": metadata.get("country", "")
        })

        for idx, entry in curations.items():
            curation_rows.append({
                "User": user,
                "Index": idx,
                "Taboo": entry["taboo"],
                "Meaning": entry["meaning"],
                "Label": entry["label"],
                "Timestamp": entry["timestamp"]
            })

    if progress_data:
        st.subheader("📊 User Progress Overview")
        st.dataframe(pd.DataFrame(progress_data))

    if metadata_rows:
        st.subheader("👤 User Metadata")
        metadata_df = pd.DataFrame(metadata_rows)
        st.dataframe(metadata_df)
        st.download_button(
            "📥 Download Metadata (CSV)",
            metadata_df.to_csv(index=False).encode("utf-8"),
            "user_metadata.csv",
            "text/csv"
        )

    if curation_rows:
        st.subheader("📜 Taboo Data")
        curation_df = pd.DataFrame(curation_rows)
        st.dataframe(curation_df)
        st.download_button(
            "📥 Download Taboo Data (CSV)",
            curation_df.to_csv(index=False).encode("utf-8"),
            "taboo_data.csv",
            "text/csv"
        )


# -----------------------------
# Main App
# -----------------------------
def main():
    st.title("🌍 Taboo Data Curation Platform")

    if "username" not in st.session_state:
        st.session_state.username = None
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "page" not in st.session_state:
        st.session_state.page = "Login"

    menu = ["Login", "Metadata", "Curate", "Admin", "Refresh", "About"]
    choice = st.sidebar.selectbox("Menu", menu, index=menu.index(st.session_state.page))
    st.session_state.page = choice

    if st.session_state.page == "Login":
        if not st.session_state.logged_in:
            username = st.text_input("Enter your username")
            if st.button("Login"):
                if username.strip():
                    st.session_state.username = username.strip()
                    st.session_state.logged_in = True
                    st.success(f"🎉 Welcome, {username}!")
                    st.session_state.page = "Metadata"
                    st.rerun()
                else:
                    st.error("Please enter a valid username.")
        else:
            st.info(f"✅ Logged in as {st.session_state.username}")
            if st.button("Next →"):
                st.session_state.page = "Metadata"
                st.rerun()

    elif st.session_state.page == "Metadata":
        if st.session_state.logged_in:
            metadata_page(st.session_state.username)
        else:
            st.warning("Please login first.")

    elif st.session_state.page == "Curate":
        if st.session_state.logged_in:
            curation_page(st.session_state.username)
        else:
            st.warning("Please login first.")

    elif st.session_state.page == "Admin":
        admin_page()

    elif st.session_state.page == "Refresh":
        st.session_state.clear()
        st.success("🔄 App refreshed.")
        st.rerun()

    elif st.session_state.page == "About":
        st.subheader("ℹ️ About This App")
        st.write("""
        This is a **Taboo Data Curation Web App** built with Streamlit.  
        - Users log in, provide metadata, and curate taboo data in **three fields**: Taboo, Meaning, and Label.  
        - Data is stored securely and **only Admin can view/download it**.  
        - Admin can log in securely, monitor user progress, and download both **metadata** and **taboo data** separately.  
        - Built for collaborative cultural resource creation 🌍.
        """)


if __name__ == "__main__":
    main()
