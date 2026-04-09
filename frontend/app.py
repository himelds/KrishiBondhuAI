import streamlit as st

from backend.weather import get_weather
from backend.location import get_location
from backend.gemma import get_advice
from backend.tts import text_to_speech

st.title("🌾 কৃষি বন্ধু AI")

st.write("ফসলের ছবি আপলোড করুন এবং কৃষি পরামর্শ পান")

# Upload image
image = st.file_uploader("📸 ছবি আপলোড করুন", type=["jpg", "png"])

if image:
    st.image(image, caption="আপলোড করা ছবি", use_column_width=True)

    st.info("⏳ বিশ্লেষণ করা হচ্ছে...")

    # Step 1: Location
    location = get_location()

    # Step 2: Weather
    weather = get_weather(location["lat"], location["lon"])

    # Step 3: Prepare input for Gemma
    data = {
        "image": image,
        "weather": weather
    }

    # Step 4: AI reasoning (Gemma)
    advice = get_advice(data)

    # Step 5: Convert to speech
    audio = text_to_speech(advice)

    st.divider()

    # Output sections
    st.subheader("📋 ফলাফল")

    st.write(advice)

    st.audio(audio)

else:
    st.warning("দয়া করে একটি ছবি আপলোড করুন")