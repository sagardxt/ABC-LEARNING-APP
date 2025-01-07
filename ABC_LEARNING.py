import streamlit as st
from gtts import gTTS
import os
import speech_recognition as sr

# Function to add a persistent background image
def add_bg_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({image_url});
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        button {{
            background-color: #4CAF50;
            border-radius: 10px;
            padding: 10px;
            font-size: 18px;
            color: white;
            border: none;
            cursor: pointer;
        }}
        button:hover {{
            background-color: #45a049;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Function to generate text-to-speech audio dynamically
def generate_audio(text, filename):
    tts = gTTS(text)
    tts.save(filename)

# Function to recognize speech in real-time
def recognize_live_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening... Speak now!")
        try:
            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            return f"Could not request results; {e}"
        except Exception as e:
            return f"Error: {e}"

# Function to check if the user spoke the correct word for the image shown
def check_spoken_word(correct_word):
    st.write(f"Please speak the word that corresponds to the image shown.")
    spoken_text = recognize_live_speech()
    st.write(f"**You said:** {spoken_text}")
    if spoken_text.strip().lower() == correct_word.lower():
        st.success(f"Correct! 🎉 You correctly identified the word '{correct_word}'.")
    else:
        st.error(f"Incorrect! ❌ The correct word is '{correct_word}'.")

# Function to check the spelling of the word
def check_spelling_word(correct_word):
    st.write(f"Please spell the word '{correct_word}' by speaking each letter.")
    spoken_text = recognize_live_speech()
    st.write(f"**You said:** {spoken_text}")
    if spoken_text.strip().lower() == correct_word.lower():
        st.success(f"Correct spelling! 🎉 You spelled the word '{correct_word}' correctly.")
    else:
        st.error(f"Incorrect spelling. ❌ The correct spelling is '{correct_word}'.")

# List of letters, words, and image URLs from A to Z
letters = [
    ("A", "Apple", "https://upload.wikimedia.org/wikipedia/commons/1/15/Red_Apple.jpg"),
    ("B", "Ball", "https://upload.wikimedia.org/wikipedia/commons/7/7a/Basketball.png"),
    ("C", "Cat", "https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg"),
    ("D", "Dog", "https://upload.wikimedia.org/wikipedia/commons/d/d9/Collage_of_Nine_Dogs.jpg"),
    ("E", "Elephant", "https://upload.wikimedia.org/wikipedia/commons/3/37/African_Bush_Elephant.jpg"),
    ("F", "Fish", "https://upload.wikimedia.org/wikipedia/commons/2/24/Fish_icon.svg"),
    ("G", "Giraffe", "https://upload.wikimedia.org/wikipedia/commons/e/ec/Giraffe_picture.jpg"),
    ("H", "Hat", "https://upload.wikimedia.org/wikipedia/commons/c/cc/Red_hat.jpg"),
    ("I", "Ice Cream", "https://upload.wikimedia.org/wikipedia/commons/9/91/Ice_cream_cone.jpg"),
    ("J", "Jug", "https://upload.wikimedia.org/wikipedia/commons/2/2a/Jug_icon.png"),
    ("K", "Kite", "https://upload.wikimedia.org/wikipedia/commons/0/04/Kite_icon.svg"),
    ("L", "Lion", "https://upload.wikimedia.org/wikipedia/commons/a/a0/Lion_icon.png"),
    ("M", "Monkey", "https://upload.wikimedia.org/wikipedia/commons/5/56/Monkey_icon.png"),
    ("N", "Nest", "https://upload.wikimedia.org/wikipedia/commons/a/a7/Nest_icon.svg"),
    ("O", "Orange", "https://upload.wikimedia.org/wikipedia/commons/4/43/Orange_icon.svg"),
    ("P", "Pencil", "https://upload.wikimedia.org/wikipedia/commons/3/37/Pencil_icon.svg"),
    ("Q", "Queen", "https://upload.wikimedia.org/wikipedia/commons/d/d4/Queen_icon.svg"),
    ("R", "Rainbow", "https://upload.wikimedia.org/wikipedia/commons/7/7e/Rainbow_icon.png"),
    ("S", "Sun", "https://upload.wikimedia.org/wikipedia/commons/a/a3/Sun_icon.svg"),
    ("T", "Tree", "https://upload.wikimedia.org/wikipedia/commons/1/17/Tree_icon.png"),
    ("U", "Umbrella", "https://upload.wikimedia.org/wikipedia/commons/7/74/Umbrella_icon.png"),
    ("V", "Violin", "https://upload.wikimedia.org/wikipedia/commons/d/df/Violin_icon.svg"),
    ("W", "Whale", "https://upload.wikimedia.org/wikipedia/commons/2/2f/Whale_icon.png"),
    ("X", "Xylophone", "https://upload.wikimedia.org/wikipedia/commons/e/ef/Xylophone_icon.png"),
    ("Y", "Yarn", "https://upload.wikimedia.org/wikipedia/commons/0/04/Yarn_icon.svg"),
    ("Z", "Zebra", "https://upload.wikimedia.org/wikipedia/commons/c/c6/Zebra_icon.svg"),
]

# Initialize session state for current word index
if "current_index" not in st.session_state:
    st.session_state["current_index"] = 0

# Add Title
st.title("ABC Learning")

# Dropdown to choose an activity
option = st.selectbox("Choose an activity:", ["Select", "Learn ABC", "Play Counting Game", "Progress Report"])

# "Learn ABC" Section
if option == "Learn ABC":
    st.subheader("Learn ABC")
    current_index = st.session_state["current_index"]

    # Display current word and image
    letter, word, image_url = letters[current_index]
    st.image(image_url, caption=f"{letter} for {word}", width=300)
    st.write(f"### **{word}**")

    # Text-to-speech button (Listen to the word)
    audio_file = f"{word.lower()}_audio.mp3"
    if not os.path.exists(audio_file):
        generate_audio(word, audio_file)
    if st.button("🔊 Listen to the word", key="listen_word"):
        st.audio(audio_file)

    # Speech recognition button to check if the user spoke the word correctly
    if st.button("🎤 Speak the word", key="speak_word"):
        check_spoken_word(word)

    # Button to check spelling of the word
    if st.button("🔤 Spell the word", key="spell_word"):
        check_spelling_word(word)

    # Next button to move to the next letter
    if st.button("Next", key="next"):
        st.session_state["current_index"] = (current_index+1) % len(letters)

# "Play Counting Game" Section
elif option == "Play Counting Game":
    st.subheader("Play Counting Game")
    st.write("Counting game will be here soon!")

# "Progress Report" Section
elif option == "Progress Report":
    st.subheader("Progress Report")
    st.write("Progress report will be here soon!")

else:
    st.write("Choose an activity from the dropdown above.")
