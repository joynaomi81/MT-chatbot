import streamlit as st
import pandas as pd

# GitHub raw dataset URL
DATA_URL = "https://raw.githubusercontent.com/joynaomi81/MT-chatbot/main/healthcare_yoruba%20(1).csv"

st.set_page_config(page_title="MT Chatbot Annotation Tool", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_URL)

df = load_data()

# --- Simple User Login ---
if "user" not in st.session_state:
    st.session_state["user"] = None

if st.session_state["user"] is None:
    st.sidebar.title("🔑 Login")
    username = st.sidebar.text_input("Enter your name:")
    if st.sidebar.button("Login"):
        if username.strip():
            st.session_state["user"] = username.strip()
            st.success(f"Welcome, {st.session_state['user']}!")
        else:
            st.warning("Please enter a valid name.")
    st.stop()

# --- Keep track of current row ---
if "current_index" not in st.session_state:
    st.session_state["current_index"] = 0

# --- Sidebar Menu ---
st.sidebar.title("📌 Menu")
menu = st.sidebar.radio(
    "Choose a page:",
    ["Annotate Data", "Progress Dashboard", "User Info"]
)

# --- Annotation Page ---
if menu == "Annotate Data":
    st.title("📊 Data Annotation Tool")

    index = st.session_state["current_index"]

    if index >= len(df):
        st.success("🎉 You have finished annotating all rows!")
    else:
        row = df.iloc[index]

        st.write(f"### Row {index + 1} of {len(df)}")
        st.write("**English Prompt:**")
        st.info(row["prompt"])

        yoruba_prompt = st.text_area("Edit Yoruba Prompt if needed:", row["prompt_translated"], height=100, key="prompt_input")

        st.write("**English Completion:**")
        st.info(row["completion"])

        yoruba_completion = st.text_area("Edit Yoruba Completion if needed:", row["completion_translated"], height=100, key="completion_input")

        if st.button("💾 Save & Next"):
            df.at[index, "prompt_translated"] = yoruba_prompt
            df.at[index, "completion_translated"] = yoruba_completion
            df.at[index, "annotator"] = st.session_state["user"]

            st.success(f"Row {index} saved by {st.session_state['user']}!")
            st.session_state["current_index"] += 1
            st.experimental_rerun()  # reload app at next row

    st.download_button("⬇️ Download Updated CSV", df.to_csv(index=False), file_name="annotated_mt.csv")

# --- Progress Dashboard ---
elif menu == "Progress Dashboard":
    st.title("📈 Annotation Progress")

    total = len(df)
    done = ((df["prompt_translated"].notna()) & (df["completion_translated"].notna())).sum()

    st.metric("Total Rows", total)
    st.metric("Annotated", done)
    st.metric("Remaining", total - done)

    if total > 0:
        progress_value = min(max(done / total, 0.0), 1.0)
        st.progress(progress_value)
        st.write(f"Progress: {progress_value:.0%}")
    else:
        st.progress(0)

    if "annotator" in df.columns:
        st.write("### Per User Progress")
        progress_table = df.groupby("annotator").apply(
            lambda x: ((x["prompt_translated"].notna()) & (x["completion_translated"].notna())).sum()
        )
        st.table(progress_table)

# --- User Info Page ---
elif menu == "User Info":
    st.title("👤 User Info")
    st.write(f"Logged in as: **{st.session_state['user']}**")
    if st.button("Logout"):
        st.session_state["user"] = None
        st.session_state["current_index"] = 0
        st.rerun()
