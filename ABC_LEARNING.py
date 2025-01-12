import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from gtts import gTTS
import os
import speech_recognition as sr

import random
from PIL import Image

from time import time
from random import randint, shuffle
from datetime import datetime
import pickle
import bisect
from groq import Groq


# Path to images directory
vegetable_images_path = r"C:\Users\ASUS\Documents\vegetable_images"

# List of vegetable image filenames (ensure these images exist in the folder)
vegetable_images = [
    'brinjal.jpg', 'cabbage.jpg', 'potato.jpg', 'tomato.jpg',
    'capsicum.jpg', 'onion.jpg', 'carrot.jpg', 'radish.jpg'
]



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
            audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=5)
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
#def check_spelling_word(correct_word):
#    st.write(f"Please spell the word '{correct_word}' by speaking each letter.")
#   spoken_text = recognize_live_speech()
#    st.write(f"**You said:** {spoken_text}")
#    if spoken_text.strip().lower() == correct_word.lower():
#        st.success(f"Correct spelling! 🎉 You spelled the word '{correct_word}' correctly.")
#    else:
#        st.error(f"Incorrect spelling. ❌ The correct spelling is '{correct_word}'.")



# Load data from Google Sheets (example URL)
# You should replace with your own Google Sheets URL
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1s8BLc8CNyWAN9u2gJPJZx9Zqs5mc7VR3RgfVM_yMHQk/export?format=csv&id=1s8BLc8CNyWAN9u2gJPJZx9Zqs5mc7VR3RgfVM_yMHQk&gid=0"
    return pd.read_csv(url)


# Load the dataset
df = load_data()

# Check the structure of the dataset to help with visualization
#st.write(df.head())  # Display first few rows to check the data




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
st.title("Educational")


# Dropdown to choose an activity
option = st.selectbox("Choose an activity:", ["Select", "Learn ABC", "Play Counting Game","Maths for kids","Animal Learning","Progress Report"])



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
    #if st.button("🔤 Spell the word", key="spell_word"):
    #    check_spelling_word(word)

    # Next button to move to the next letter
    if st.button("Next", key="next"):
        st.session_state["current_index"] = (current_index+1) % len(letters)



# "Play Counting Game" Section
elif option == "Play Counting Game":
    # Function to display images and ask user to count the vegetables
    def count_vegetables(difficulty='easy'):
        if 'selected_images' not in st.session_state or 'options' not in st.session_state:
            # Determine the number of images based on the selected difficulty
            num_images = random.randint(1, 5) if difficulty == 'easy' else random.randint(6, 10)
            
            # Select random images
            selected_images = random.sample(vegetable_images, num_images)

            # Store the selected images and their count in session state
            st.session_state.selected_images = selected_images
            st.session_state.correct_count = len(selected_images)

            # Generate 4 unique options (including the correct one)
            options = {st.session_state.correct_count}
            while len(options) < 4:
                random_option = st.session_state.correct_count + random.randint(-1, 2)
                options.add(random_option)

            st.session_state.options = list(options)

        # Display the selected vegetable images in a row
        st.subheader("Guess how many vegetables you see:")
        cols = st.columns(len(st.session_state.selected_images))  # Create columns for each image
        image_paths = [os.path.join(vegetable_images_path, img) for img in st.session_state.selected_images]
        
        for i, image_path in enumerate(image_paths):
            with cols[i]:
                st.image(image_path, width=150)  # Resize each image to fit the columns

        correct_count = st.session_state.correct_count

        # Display options as radio buttons for user to select
        selected_option = st.radio(
            "How many vegetables do you see in the above images?", 
            st.session_state.options, 
            key=f"radio_button_{str(st.session_state.selected_images)}_{st.session_state.correct_count}"  # Unique key with images and count
        )

        # Handle the user's response when they click 'Submit'
        if st.button('Submit'):
            if selected_option == correct_count:
                st.success(f"Correct! There are {correct_count} vegetables!")
            else:
                st.error(f"Incorrect. There are {correct_count} vegetables. Try again!")

        # Continue button to generate a new question
        if st.button('Next Question'):
            # Clear the session state for a new question
            st.session_state.pop('selected_images', None)
            st.session_state.pop('options', None)
            st.session_state.pop('correct_count', None)
            count_vegetables(difficulty=difficulty)  # Regenerate new question

    # Main function to select difficulty level and start the game
    def select_difficulty():
        st.markdown("""
            Welcome to the Vegetable Counting Game! 🥕🥔🍅
            Your goal is to count how many vegetables are shown in the images.
        """)

        # Add Quit button
        if st.button("Quit"):
            st.warning("You have exited the game. Thank you for playing!")
            st.stop()  # Stops execution of further code

        difficulty = st.radio("Select Difficulty Level", ["Easy", "Medium"], key="difficulty_radio")
        count_vegetables(difficulty=difficulty.lower())

    # Streamlit app execution starts here
    st.title("Vegetable Counting Game")
    st.markdown("### Can you count all the vegetables?")

    # Run the game
    select_difficulty()

# "Maths for kids" Section
elif option == "Maths for kids":
    # Constants
    NTIMES = 10
    SUBTRACTION = True
    LO = 0
    HI = 10
    HIGHSCORE_FNAME = "highscores"

    # HighScores Class
    class HighScores:
        def __init__(self):
            self.scores = []
            self.num_scores = 10

        def update(self, score):
            """Add a score to the list of high scores.
            Return True if this score is among the top scores, otherwise False.
            """
            if len(self.scores) < self.num_scores:
                self.scores.append(score)
                self.scores.sort()
                return True
            index = bisect.bisect(self.scores, score)
            if index < self.num_scores:
                self.scores.insert(index, score)
                self.scores.pop()
                return True
            return False

        def __str__(self):
            return "\n".join([f"{i + 1:2d}) {score:.2f} sec" for i, score in enumerate(self.scores)])

    # Helper Functions
    def load_scores():
        try:
            with open(HIGHSCORE_FNAME, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return HighScores()


    def save_scores(scores):
        with open(HIGHSCORE_FNAME, 'wb') as f:
            pickle.dump(scores, f)


    def generate_question():
        a = randint(LO, HI)
        b = randint(LO, HI)
        do_subtraction = SUBTRACTION and bool(randint(0, 1))

        if do_subtraction:
            question = f"{a + b} - {b} = ?"
            correct_answer = a
        else:
            question = f"{a} + {b} = ?"
            correct_answer = a + b

        options = [correct_answer]
        while len(options) < 4:
            wrong_answer = randint(LO - 5, HI + 5)
            if wrong_answer != correct_answer:
                options.append(wrong_answer)

        shuffle(options)
        return question, options, correct_answer

    # Initialize Session State
    if "score" not in st.session_state:
        st.session_state.update({
            "score": 0,
            "start_time": None,
            "message": "",
            "current_question": None,
            "correct_answer": None,
            "answered": False,
            "option_selected": None,
        })

    # Header and Theme
    st.title("🎉 Fun Maths Game for Kids! 🎈")
    st.markdown(
        """Welcome to the **Maths Game**! Solve the questions and try to get the fastest score.
        
        🧮 Add or subtract numbers, pick the correct answer, and see if you can make it to the **High Scores**! Good luck!
        """
    )

    st.image("https://via.placeholder.com/800x200.png?text=Welcome+to+the+Maths+Adventure!", use_column_width=True)

    # Start the Game
    if st.session_state.start_time is None:
        st.session_state.start_time = time()

    # Generate a Question
    if st.session_state.score < NTIMES and st.session_state.current_question is None:
        question, options, correct_answer = generate_question()
        st.session_state.current_question = (question, options)
        st.session_state.correct_answer = correct_answer

    # Display the Question
    if st.session_state.current_question:
        question, options = st.session_state.current_question

        st.header(f"🦄 Question {st.session_state.score + 1}:")
        st.subheader(question)

        option_selected = st.radio("Choose your answer:", options, key=f"q{st.session_state.score}")

        if st.button("🐾 Submit Answer") and not st.session_state.answered:
            st.session_state.option_selected = option_selected
            st.session_state.answered = True

        if st.session_state.answered:
            if st.session_state.option_selected == st.session_state.correct_answer:
                st.success("🎉 Hooray! That's correct! You're amazing! 🐻")
                st.balloons()
                st.session_state.score += 1
            else:
                st.error(f"❌ Oh no! The correct answer is {st.session_state.correct_answer}. Keep going, you got this! 🐢")
            
            st.write(f"🌟 Your current score: {st.session_state.score}/{NTIMES}")

            if st.button("🔄 Next Question"):
                st.session_state.answered = False
                st.session_state.current_question = None

    # End of Game
    if st.session_state.score == NTIMES:
        elapsed = time() - st.session_state.start_time
        st.balloons()
        st.image("https://via.placeholder.com/800x200.png?text=You+Did+It!", use_column_width=True)
        st.write(f"🎯 **Fantastic!** You completed the game in {elapsed:.2f} seconds! 🏆")

        highscores = load_scores()
        if highscores.update(elapsed):
            st.success(f"🏅 Congratulations! You made it to the top {highscores.num_scores} scores!")

        st.write("📜 **High Scores:**")
        st.text(highscores)
        save_scores(highscores)

        st.write("🎉 **Your Score:**")
        st.write(f"⏱️ Time: {elapsed:.2f} seconds")

        st.session_state.score = 0
        st.session_state.start_time = None
        st.session_state.current_question = None

    # Quit Button
    if st.button("🚪 Quit"):
        st.session_state.score = 0
        st.session_state.start_time = None
        st.write("🚪 Game has been quit. Refresh the page to restart.")

# "Animal Learning" Section
elif option == "Animal Learning":
    # Constants and Paths
    DATASET_PATH = r"C:\Users\ASUS\Documents\animal_dataset.csv"
    DATA_FILE_PATH = r"C:\Users\ASUS\Documents\animal_dataset.csv"
    MYSQL_CONFIG = {
    "host": '127.0.0.1',
    "user": 'root',
    "password": '9545883002@Sj',
    "database": 'customer'
    }

    # Load dataset
    animal_data = pd.read_csv(DATASET_PATH)

    # Utility Functions
    def get_animal_details(category):
        """Fetch animals and details based on category."""
        return animal_data[animal_data["animal_category"].str.lower() == category.lower()]

    def fetch_characteristics(animal, number_char):
        """Fetch animal characteristics using Groq API."""
        client = Groq(api_key="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")
        try:
            chat_completion = client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": f"""You are an expert teacher for children below age 5, to teach them characteristics for animal 
                    Please describe {number_char} of {animal} in a numbered list. each characteristic in 5-6 words."""
                }],
                model="llama-3.3-70b-versatile",
            )
            return chat_completion.choices[0].message.content.split("\n")
        except Exception as e:
            st.error(f"Error fetching characteristics: {e}")
            return []

    def generate_audio(text):
        """Generate audio from text and return base64 string."""
        try:
            tts = gTTS(text, lang="en")
            audio_file_path = "temp_audio.mp3"
            tts.save(audio_file_path)

            # Read and encode the audio file to base64
            with open(audio_file_path, "rb") as f:
                audio_bytes = f.read()
                b64_audio = base64.b64encode(audio_bytes).decode()

            os.remove(audio_file_path)
            return b64_audio
        except Exception as e:
            st.error(f"Error generating audio: {e}")
            return None

    def update_mysql_table(animal_name, is_correct, category):
        """Insert new entry into MySQL table with animal performance data."""
        try:
            conn = mysql.connector.connect(**MYSQL_CONFIG)
            cursor = conn.cursor()

            # Create table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS animal_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    animal_name VARCHAR(255),
                    category VARCHAR(255),
                    attempt INT DEFAULT 0,
                    correct INT DEFAULT 0,
                    incorrect INT DEFAULT 0,
                    timestamps TEXT,
                    dates TEXT
                )
            """)

            current_timestamp = datetime.now().timestamp()
            current_date = datetime.now().date()

            # Always insert a new record
            cursor.execute("""
                INSERT INTO animal_data (animal_name, category, attempt, correct, incorrect, timestamps, dates)
                VALUES (%s, %s, 1, %s, %s, %s, %s)
            """, (animal_name, category, 1 if is_correct else 0, 0 if is_correct else 1, current_timestamp, current_date))

            conn.commit()
        except mysql.connector.Error as e:
            st.error(f"Error inserting data into MySQL table: {e}")
        finally:
            cursor.close()
            conn.close()

    def recognize_speech():
        """Recognize speech using microphone input."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... Please say the animal's name.")
            audio_data = recognizer.listen(source)
            try:
                return recognizer.recognize_google(audio_data).lower()
            except (sr.UnknownValueError, sr.RequestError) as e:
                st.error("Could not understand or request failed. Please try again.")
                return None

    # Pages
    def home_page():
        st.title("Animal Sounds Learning Application")
        st.subheader("Choose a Category:")
        categories = ["Farm Animal", "Sea Creature", "Bird", "Wild Animal", "Jungle Animal"]
        for i, category in enumerate(categories):
            if st.button(category):
                st.session_state.selected_category = category.lower()
                st.session_state.page_index = i + 1
                break

    def animal_page(category):
        """Display animal page with selected category."""
        st.title(f"{category} Animals")
        animals = get_animal_details(category)
        if animals.empty:
            st.error(f"No {category.lower()} found in the dataset.")
            return

        animal_names = animals["animal_name"].tolist()
        selected_animal_name = st.selectbox("Select an Animal:", animal_names)
        selected_animal = animals[animals["animal_name"] == selected_animal_name].iloc[0]

        try:
            st.image(selected_animal["url"], caption=selected_animal["animal_name"])
        except Exception:
            st.error(f"Failed to load image for {selected_animal_name}.")

        if st.button("Play Sound"):
            b64_audio = generate_audio(selected_animal_name)
            if b64_audio:
                st.markdown(f'<audio autoplay style="display:none;"><source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3"></audio>', unsafe_allow_html=True)

        if st.button(f"Try Saying Here"):
            recognized_text = recognize_speech()
            if recognized_text:
                is_correct = recognized_text == selected_animal_name.lower()
                st.session_state.test_attempts.append({"animal": selected_animal_name, "recognized_text": recognized_text, "is_correct": is_correct})

                if is_correct:
                    st.success(f"Correct! You said '{selected_animal_name}'.")
                else:
                    st.error(f"Incorrect. You said '{recognized_text}'. Try again.")

                update_mysql_table(selected_animal_name, is_correct, category)

        num_characteristics = st.selectbox("Select number of characteristics to display:", list(range(1, 21)))
        st.session_state.num_characteristics = num_characteristics

        st.subheader(f"Learn About {selected_animal_name}")

        if st.button(f"Learn Characteristics of {selected_animal_name}"):
            characteristics = fetch_characteristics(selected_animal_name, num_characteristics)
            if characteristics:
                st.write("\n".join([f"{i+1}. {characteristic}" for i, characteristic in enumerate(characteristics)]))

    # Page Routing Logic
    if "page_index" not in st.session_state:
        st.session_state.page_index = 0
        home_page()
    elif st.session_state.page_index == 0:
        home_page()
    else:
        categories = ["Farm Animal", "Sea Creature", "Bird", "Wild Animal", "Jungle Animal"]
        category = categories[st.session_state.page_index - 1]
        animal_page(category)

                


# "Progress Report" Section
if option == "Progress Report":
    st.subheader("Progress Report")

    # Check if the data has been loaded correctly
    if df.empty:
        st.write("No data available.")
    else:
        # Extract the relevant columns for clicks (Click_A to Click_Z)
        letter_columns = [col for col in df.columns if col.startswith('Click_')]  # Click_A to Click_Z

        # Bar chart for Child clicks on each letter
        st.write("### Clicks on Each Letter by Child (Name)")
        fig_bar = px.bar(df, x="Name", y=letter_columns, title="Clicks on Each Letter")
        st.plotly_chart(fig_bar)

        # Pie chart showing distribution of clicks on each letter
        st.write("### Distribution of Clicks for Each Letter")
        for letter in letter_columns:
            fig_pie = px.pie(df, names=letter, title=f"Distribution of Clicks for Letter {letter}")
            st.plotly_chart(fig_pie)

        # Line chart for progress over time (assuming 'Date' is the time column)
        if "Date" in df.columns:
            for letter in letter_columns:
                fig_line = px.line(df, x="Date", y=letter, title=f"Progress in Letter {letter} Over Time")
                st.plotly_chart(fig_line)

        # Additional Insights
        st.write("### Additional Insights")
        st.write(f"Total number of children: {df['Name'].nunique()}")
        st.write(f"Letters in the report: {', '.join(letter_columns)}")

        # Option to download the full dataset
        st.download_button(
            label="Download Full Dataset",
            data=df.to_csv(),
            file_name="Full_Progress_Report.csv",
            mime="text/csv"
        )

        # Display the detailed progress report in a table format
        st.write("### Detailed Progress Report")
        st.write(df)



    
else:
    st.write("Choose an activity from the dropdown above.")
