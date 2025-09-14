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
        ["Home", "Stories", "Add Your Story", "Quiz", "African Languages", "About"],
        icons=["house", "book", "plus-circle", "question-circle", "languages", "info-circle"],
        menu_icon="cast",
        default_index=0,
    )

# Page content
if selected == "Home":
    st.title("🌍 Welcome to the African Stories App ✨")
    st.write("Preserving African culture through storytelling.")
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/0/0c/African_storytelling.jpg", 
        use_container_width=True
    )

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

elif selected == "African Languages":
    st.title("🗣️ African Languages")
    st.write("Explore greetings, proverbs, and folktales in African languages.")

    language = st.selectbox("Choose a language:", ["Yoruba", "Swahili", "Hausa", "Zulu", "Igbo"])

    if language == "Yoruba":
        st.subheader("Yoruba (Nigeria)")
        st.write("👋 Hello: **Bawo ni**")
        st.write("🙏 Thank you: **E se**")
        st.write("💡 Proverb: **Ìjángbọ̀n kì í tán nílẹ́ ayé.** (Conflict never ends in the world.)")
        st.write("📖 Folktale: Once upon a time, a tortoise tricked the birds to attend a feast in the sky...")

    elif language == "Swahili":
        st.subheader("Swahili (East Africa)")
        st.write("👋 Hello: **Hujambo**")
        st.write("🙏 Thank you: **Asante**")
        st.write("💡 Proverb: **Haraka haraka haina baraka.** (Hurry hurry has no blessings.)")
        st.write("📖 Folktale: Long ago, the hare tricked the mighty lion in a small coastal village...")

    elif language == "Hausa":
        st.subheader("Hausa (West Africa)")
        st.write("👋 Hello: **Sannu**")
        st.write("🙏 Thank you: **Nagode**")
        st.write("💡 Proverb: **Komai nisan jifa, ƙasa zai dawo.** (No matter how far you throw it, it will land on the ground.)")
        st.write("📖 Folktale: The hyena and the hare once set out on a journey, but greed betrayed the hyena...")

    elif language == "Zulu":
        st.subheader("Zulu (South Africa)")
        st.write("👋 Hello: **Sawubona**")
        st.write("🙏 Thank you: **Ngiyabonga**")
        st.write("💡 Proverb: **Umuntu ngumuntu ngabantu.** (A person is a person through other people.)")
        st.write("📖 Historical Story: King Shaka Zulu transformed the Zulu kingdom into a powerful nation...")

    elif language == "Igbo":
        st.subheader("Igbo (Nigeria)")
        st.write("👋 Hello: **Kedu**")
        st.write("🙏 Thank you: **Imela**")
        st.write("💡 Proverb: **Otu osisi adịghị eme ọhịa.** (One tree does not make a forest.)")
        st.write("📖 Folktale: The tortoise, known for his cunning, once tricked the birds into giving him feathers to fly...")

elif selected == "About":
    st.title("ℹ️ About This App")
    st.write("""
        This app is designed to showcase African culture through stories, folktales, 
        proverbs, history, and languages. Users can contribute their own stories, 
        learn simple African language phrases, and test their knowledge with a quiz!
    """)
