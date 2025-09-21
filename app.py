import streamlit as st
import pandas as pd
import os

DATA_PATH = "dataset.csv"

# Load dataset
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
else:
    st.error("https://raw.githubusercontent.com/joynaomi81/Medical-Terminologies/refs/heads/main/healthcare_yoruba%20.csv?token=GHSAT0AAAAAADIBOALWVG4YXENASBWRBJ5W2GQRQ3A")
    st.stop()

# Add annotation columns if not exist
for col in ["corrected_yoruba_prompt", "corrected_yoruba_completion",
            "prompt_status", "completion_status", "annotator"]:
    if col not in df.columns:
        if col in ["prompt_status", "completion_status"]:
            df[col] = "Unchecked"
        else:
            df[col] = ""

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

# --- Sidebar Menu ---
st.sidebar.title("📌 Menu")
menu = st.sidebar.radio(
    "Choose a page:",
    ["Annotate Data", "Progress Dashboard", "User Info"]
)

# --- Annotation Page ---
if menu == "Annotate Data":
    st.title("📊 Data Annotation Tool")

    # Navigation
    index = st.number_input("Go to row:", min_value=0, max_value=len(df)-1, value=0, step=1)
    row = df.iloc[index]

    st.write(f"### Row {index}")
    st.write("**English Prompt:**")
    st.info(row["english_prompt"])

    # Yoruba prompt annotation
    st.write("**Yoruba Prompt:**")
    yoruba_prompt = st.text_area("Edit Yoruba Prompt if needed:", 
                                 row["corrected_yoruba_prompt"] or row["yoruba_prompt"], height=100)
    prompt_status = st.radio("Prompt Status:", ["Correct", "Incorrect"], 
                             index=0 if row["prompt_status"]=="Correct" else 1)

    # English completion
    st.write("**English Completion:**")
    st.info(row["english_completion"])

    # Yoruba completion annotation
    st.write("**Yoruba Completion:**")
    yoruba_completion = st.text_area("Edit Yoruba Completion if needed:", 
                                     row["corrected_yoruba_completion"] or row["yoruba_completion"], height=100)
    completion_status = st.radio("Completion Status:", ["Correct", "Incorrect"], 
                                 index=0 if row["completion_status"]=="Correct" else 1)

    # Save edits
    if st.button("💾 Save Annotation"):
        df.at[index, "corrected_yoruba_prompt"] = yoruba_prompt
        df.at[index, "prompt_status"] = prompt_status
        df.at[index, "corrected_yoruba_completion"] = yoruba_completion
        df.at[index, "completion_status"] = completion_status
        df.at[index, "annotator"] = st.session_state["user"]
        df.to_csv(DATA_PATH, index=False)
        st.success(f"Row {index} saved by {st.session_state['user']}!")

# --- Progress Dashboard ---
elif menu == "Progress Dashboard":
    st.title("📈 Annotation ")

    total = len(df)
    done = (df["prompt_status"] != "Unchecked").sum()
    st.metric("Total Rows", total)
    st.metric("Annotated", done)
    st.metric("Remaining", total - done)

    st.progress(done / total)

    st.write("### Per User Progress")
    progress_table = df.groupby("annotator")["prompt_status"].apply(lambda x: (x!="Unchecked").sum())
    st.table(progress_table)

# --- User Info Page ---
elif menu == "User Info":
    st.title("👤 User Info")
    st.write(f"Logged in as: **{st.session_state['user']}**")
    if st.button("Logout"):
        st.session_state["user"] = None
        st.rerun()
