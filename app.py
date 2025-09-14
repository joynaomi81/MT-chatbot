import streamlit as st
from streamlit_option_menu import option_menu

# App settings
st.set_page_config(page_title="African Stories App", layout="wide")

# In-memory storage
if "user_stories" not in st.session_state:
    st.session_state.user_stories = []

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "African Stories", 
        ["Home", "Stories", "Add Your Story", "Quiz", "About"],
        icons=["house", "book", "plus-circle", "question-circle", "info-circle"],
        menu_icon="cast",
        default_index=0,
    )

# Page content
if selected == "Home":
    st.title("🌍 Welcome to the African Stories App ✨")
    st.write("Preserving African culture through storytelling.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/0c/African_storytelling.jpg", use_column_width=True)

elif selected == "Stories":
    st.title("📖 Explore Stories")
    story_type = st.selectbox("Pick a category:", ["Folktales", "Proverbs", "Historical Stories", "User Submitted"])

    if story_type == "Folktales":
        st.subheader("🦁 Folktale: The Lion and the Hare")
        st.write("Once upon a time in an African village, the clever hare outsmarted the mighty lion...")
    
    elif story_type == "Proverbs":
        st.subheader("💡 Yoruba Proverb")
        st.write("“Bí a bá rí bí ọ̀ràn, a kìí fọ́ ẹsẹ̀ méjì wọ inú rẹ̀.” (When there is trouble, one should not rush in with both feet.)")
    
    elif story_type == "Historical Stories":
        st.subheader("⏳ Story of Queen Amina of Zazzau")
        st.write("Queen Amina was a fierce Hausa warrior queen of the city-state Zazzau...")
    
    elif story_type == "User Submitted":
        st.subheader("📝 Stories from Our Community")
        if st.session_state.user_stories:
            for idx, story in enumerate(st.session_state.user_stories, 1):
                st.markdown(f"**{idx}. {story['title']}** — *{story['author']}*")
                st.write(story['content'])
                st.markdown("---")
        else:
            st.info("No user stories yet. Be the first to add one in 'Add Your Story'!")

elif selected == "Add Your Story":
    st.title("✍️ Share Your Story")
    with st.form("story_form"):
        title = st.text_input("Story Title")
        author = st.text_input("Your Name")
        content = st.text_area("Write your story here...")
        submitted = st.form_submit_button("Submit")

        if submitted:
            if title and author and content:
                st.session_state.user_stories.append(
                    {"title": title, "author": author, "content": content}
                )
                st.success("🎉 Your story has been added!")
            else:
                st.error("Please fill in all fields.")

elif selected == "Quiz":
    st.title("❓ African Stories Quiz")
    st.write("Test your knowledge of African culture, history, and proverbs!")

    questions = [
        {
            "q": "Who was Queen Amina of Zazzau?",
            "options": ["A Yoruba goddess", "A Hausa warrior queen", "A Swahili storyteller", "An Igbo trader"],
            "answer": "A Hausa warrior queen"
        },
        {
            "q": "What animal is often portrayed as clever in African folktales?",
            "options": ["Lion", "Elephant", "Hare", "Crocodile"],
            "answer": "Hare"
        },
        {
            "q": "What does the Yoruba proverb mean: 'Bí a bá rí bí ọ̀ràn, a kìí fọ́ ẹsẹ̀ méjì wọ inú rẹ̀'?",
            "options": ["Rush into trouble", "Be cautious in trouble", "Avoid storytelling", "Respect elders"],
            "answer": "Be cautious in trouble"
        }
    ]

    score = 0
    for i, q in enumerate(questions):
        st.subheader(f"Q{i+1}: {q['q']}")
        choice = st.radio("Choose your answer:", q["options"], key=f"q{i}")
        if choice == q["answer"]:
            score += 1

    if st.button("Submit Quiz"):
        st.session_state.quiz_score = score
        st.success(f"🎉 You scored {score} out of {len(questions)}!")

elif selected == "About":
    st.title("ℹ️ About This App")
    st.write("""
        This app is designed to showcase African culture through stories, folktales, 
        proverbs, and history. Users can contribute their own stories and even 
        test their knowledge through a fun quiz!
    """)
