import streamlit as st

from backend.disease import detect_disease
from backend.weather import get_weather
from backend.location import get_location
from backend.gemma import get_advice
from backend.tts import text_to_speech

st.title("🌾 KrishiBondhu AI")

image = st.file_uploader("Upload crop image", type=["jpg", "png"])

if image:
    st.image(image)

    # Step 1: Disease detection
    disease = detect_disease(image)

    # Step 2: Location
    location = get_location()

    # Step 3: Weather
    weather = get_weather(location["lat"], location["lon"])

    # Step 4: Combine
    data = {
        "disease": disease,
        "weather": weather
    }

    # Step 5: AI Advice
    advice = get_advice(data)

    # Step 6: Voice
    audio = text_to_speech(advice)

    # Output
    st.subheader("📋 কৃষি পরামর্শ")
    st.write(advice)
    st.audio(audio)