import streamlit as st
from gtts import gTTS
import os
from PIL import Image
import base64

def add_bg_image(image_url="https://upload.wikimedia.org/wikipedia/commons/3/3d/Children_playing.jpg"):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({image_url});
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Function to generate text-to-speech audio dynamically
def generate_audio(text, filename):
    tts = gTTS(text)
    tts.save(filename)

# App title
st.title("ABC Learning")

# List of letters, words, image URLs, and background images
letters = [
    ("A", "Apple", "https://upload.wikimedia.org/wikipedia/commons/1/15/Red_Apple.jpg", "https://upload.wikimedia.org/wikipedia/commons/f/f9/Apple_tree.jpg"),
    ("B", "Ball", "https://upload.wikimedia.org/wikipedia/commons/7/7a/Basketball.png", "https://upload.wikimedia.org/wikipedia/commons/8/8b/Playground.jpg"),
    ("C", "Cat", "https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg", "https://upload.wikimedia.org/wikipedia/commons/a/a3/Cat_sitting_on_the_grass.jpg"),
    ("D", "Dog", "https://upload.wikimedia.org/wikipedia/commons/d/d9/Collage_of_Nine_Dogs.jpg", "https://upload.wikimedia.org/wikipedia/commons/6/6e/Playing_with_dogs.jpg"),
    ("E", "Elephant", "https://upload.wikimedia.org/wikipedia/commons/3/37/African_Bush_Elephant.jpg", "https://upload.wikimedia.org/wikipedia/commons/f/f9/Elephant_in_water.jpg"),
    ("F", "Fish", "https://upload.wikimedia.org/wikipedia/commons/2/2d/Goldfish3.jpg", "https://upload.wikimedia.org/wikipedia/commons/3/3e/Tropical_fish.jpg"),
    ("G", "Giraffe", "https://upload.wikimedia.org/wikipedia/commons/3/3b/Giraffe_standing.jpg", "https://upload.wikimedia.org/wikipedia/commons/6/6d/Giraffes_in_zoo.jpg"),
    ("H", "House", "https://upload.wikimedia.org/wikipedia/commons/6/65/Traditional_house_in_Norway.jpg", "https://upload.wikimedia.org/wikipedia/commons/f/fd/House_with_garden.jpg"),
    ("I", "Ice Cream", "https://upload.wikimedia.org/wikipedia/commons/a/ac/Ice_Cream_cones.jpg", "https://upload.wikimedia.org/wikipedia/commons/3/34/Ice_Cream_Parlor.jpg"),
    ("J", "Juice", "https://upload.wikimedia.org/wikipedia/commons/e/e1/Glass_of_Orange_Juice.jpg", "https://upload.wikimedia.org/wikipedia/commons/2/2b/Fruit_Juice.jpg"),
    ("K", "Kite", "https://upload.wikimedia.org/wikipedia/commons/7/76/Kite_in_sky.jpg", "https://upload.wikimedia.org/wikipedia/commons/3/36/Kite_Festival.jpg"),
    ("L", "Lion", "https://upload.wikimedia.org/wikipedia/commons/7/73/Lion_waiting_in_Namibia.jpg", "https://upload.wikimedia.org/wikipedia/commons/2/21/Lion_family.jpg"),
    ("M", "Monkey", "https://upload.wikimedia.org/wikipedia/commons/5/55/Monkey_face_closeup.jpg", "https://upload.wikimedia.org/wikipedia/commons/7/7d/Monkeys_in_forest.jpg"),
    ("N", "Nest", "https://upload.wikimedia.org/wikipedia/commons/2/28/Bird_nest_with_eggs.jpg", "https://upload.wikimedia.org/wikipedia/commons/6/65/Bird_Nest_in_tree.jpg"),
    ("O", "Orange", "https://upload.wikimedia.org/wikipedia/commons/c/c4/Orange-Fruit-Pieces.jpg", "https://upload.wikimedia.org/wikipedia/commons/e/e3/Oranges_on_tree.jpg"),
    ("P", "Parrot", "https://upload.wikimedia.org/wikipedia/commons/2/21/Parrot_closeup.jpg", "https://upload.wikimedia.org/wikipedia/commons/e/e0/Parrots_on_tree.jpg"),
    ("Q", "Queen", "https://upload.wikimedia.org/wikipedia/commons/9/9e/Queen_crown.jpg", "https://upload.wikimedia.org/wikipedia/commons/3/31/Queen_in_ceremony.jpg"),
    ("R", "Rabbit", "https://upload.wikimedia.org/wikipedia/commons/3/35/Rabbit_in_grass.jpg", "https://upload.wikimedia.org/wikipedia/commons/7/71/Rabbit_with_flowers.jpg"),
    ("S", "Sun", "https://upload.wikimedia.org/wikipedia/commons/3/3d/Sun_in_sky.jpg", "https://upload.wikimedia.org/wikipedia/commons/f/f5/Sunset_with_sun.jpg"),
    ("T", "Tree", "https://upload.wikimedia.org/wikipedia/commons/8/83/Tree_in_field.jpg", "https://upload.wikimedia.org/wikipedia/commons/c/c9/Trees_in_park.jpg"),
    ("U", "Umbrella", "https://upload.wikimedia.org/wikipedia/commons/a/a3/Umbrella_on_beach.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/9e/Colorful_Umbrellas.jpg"),
    ("V", "Van", "https://upload.wikimedia.org/wikipedia/commons/8/88/Classic_Van.jpg", "https://upload.wikimedia.org/wikipedia/commons/b/b2/Vans_on_road.jpg"),
    ("W", "Whale", "https://upload.wikimedia.org/wikipedia/commons/4/4e/Whale_in_ocean.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/56/Whale_diving.jpg"),
    ("X", "Xylophone", "https://upload.wikimedia.org/wikipedia/commons/6/6e/Xylophone.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/54/Xylophone_in_classroom.jpg"),
    ("Y", "Yacht", "https://upload.wikimedia.org/wikipedia/commons/3/3e/Yacht_in_sea.jpg", "https://upload.wikimedia.org/wikipedia/commons/1/1f/Yachts_in_harbor.jpg"),
    ("Z", "Zebra", "https://upload.wikimedia.org/wikipedia/commons/6/68/Zebra_in_safari.jpg", "https://upload.wikimedia.org/wikipedia/commons/2/2d/Zebras_in_field.jpg"),
]

# Home screen buttons
option = st.selectbox("Choose an activity:", ["Select", "Learn ABC", "Play Counting Game", "Progress Report"])

if option == "Learn ABC":
    st.subheader("Learn ABC")
    current_index = st.session_state.get('current_index', 0)

    letter, word, image_url, bg_url = letters[current_index]
    add_bg_image(bg_url)
    
    st.write(f"**{letter}**")
    st.image(image_url, caption=f"{letter} for {word}", width=150)

    col1, col2 = st.columns([1, 3])
    with col1:
        audio_file = f"{letter.lower()}_audio.mp3"
        if not os.path.exists(audio_file):
            generate_audio(f"{word}", audio_file)
        if st.button(f"🔊 Hear '{word}'", key=letter):
            st.audio(audio_file)
    with col2:
        st.write(f"### {letter} for {word}")

    if st.button("Next"):
        if current_index < len(letters) - 1:
            st.session_state['current_index'] = current_index + 1
        else:
            st.session_state['current_index'] = 0

elif option == "Play Counting Game":
    st.subheader("Play Counting Game")
    st.write("Counting game will be here soon!")

elif option == "Progress Report":
    st.subheader("Progress Report")
    st.write("Progress report will be here soon!")

else:
    st.write("Choose an activity from the dropdown above.")
