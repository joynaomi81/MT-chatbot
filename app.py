import streamlit as st
import json
import os

# -----------------------------
# Config (using secrets.toml)
# -----------------------------
ADMIN_PASSWORD = st.secrets["admin"]["password"]
DATA_FILE = "user_progress.json"


# -----------------------------
# Helpers
# -----------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# -----------------------------
# Pages
# -----------------------------
def login_page():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if password == ADMIN_PASSWORD:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid password")


def curation_page(username):
    st.subheader("📦 Taboo Curation")

    # Load user data
    all_data = load_data()
    user_data = all_data.get(username, {})

    # Ensure "curations" exists
    if "curations" not in user_data:
        user_data["curations"] = {}

    # Track how many entries are there
    curated_count = len(user_data["curations"])

    with st.form("curation_form"):
        taboo = st.text_input("Enter Taboo")
        meaning = st.text_area("Enter Meaning of the Taboo")
        label = st.text_input("Enter Label (e.g., taboo)")

        submitted = st.form_submit_button("Save")
        if submitted:
            if taboo and meaning and label:
                user_data["curations"][str(curated_count + 1)] = {
                    "taboo": taboo,
                    "meaning": meaning,
                    "label": label
                }
                all_data[username] = user_data
                save_data(all_data)
                st.success("✅ Entry saved successfully!")
                st.rerun()
            else:
                st.error("⚠️ Please fill in all fields before saving.")

    # Show user’s curated data
    if user_data["curations"]:
        st.write("### Your Curated Taboos")
        st.json(user_data["curations"])


def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_page()
    else:
        curation_page(st.session_state["username"])


if __name__ == "__main__":
    main()
