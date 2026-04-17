import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Fix path to allow importing from backend seamlessly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
load_dotenv()

from backend.weather import get_weather
from backend.location import get_location, get_precise_city
from backend.gemma import chat_with_agent, build_prompt
from backend.tts import text_to_speech
from streamlit_geolocation import streamlit_geolocation

st.set_page_config(page_title="KrishiBondhu AI", page_icon="🌾", layout="wide")

# Load CSS
css_path = os.path.join(os.path.dirname(__file__), 'style.css')
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Main Language Selection Header
col1, col2 = st.columns([1,1])
with col1:
    st.title("🌾 কৃষি বন্ধু AI")
with col2:
    st.write("") # padding
    language = st.radio("Language / ভাষা", ["বাংলা", "English"], horizontal=True)

lang_key = "bn" if language == "বাংলা" else "en"
analysis_text = "⏳ বিশ্লেষণ করা হচ্ছে..." if language == "বাংলা" else "⏳ Analyzing..."
gps_text = "📍 আপনার নিখুঁত অবস্থান জানতে বাটনে ক্লিক করুন (GPS):" if language == "বাংলা" else "📍 Click for Precise Location (GPS):"
loc_prefix = "📍 বর্তমান অবস্থান:" if language == "বাংলা" else "📍 Current Location:"
weather_prefix = "🌦️ বর্তমান আবহাওয়া:" if language == "বাংলা" else "🌦️ Current Weather:"

st.write("ফসলের ছবি আপলোড করুন এবং কৃষি পরামর্শ পান" if language == "বাংলা" else "Upload a crop image and get farming advice")

# Geolocation button
st.write(f"**{gps_text}**")
gps_location = streamlit_geolocation()

image = st.file_uploader("📸 Upload Crop Image / ছবি আপলোড করুন", type=["jpg", "png"])

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_uploader" not in st.session_state:
    st.session_state.last_uploader = None
if "current_lang" not in st.session_state:
    st.session_state.current_lang = language

if language != st.session_state.current_lang:
    st.session_state.current_lang = language
    # Automatically ask AI to translate the chat history when toggled
    if "messages" in st.session_state and len(st.session_state.messages) > 0:
        translation_cmd = "Please translate your previous advice into English." if language == "English" else "দয়া করে আপনার আগের পরামর্শগুলো বাংলায় অনুবাদ করুন।"
        st.session_state.messages.append({"role": "user", "content": translation_cmd})
        st.session_state.pending_translation = True

# Clear chat immediately if the main crop image changed!
if image is not None and image.name != st.session_state.last_uploader:
    st.session_state.messages = []
    st.session_state.last_uploader = image.name
    if "audio" in st.session_state:
        del st.session_state.audio

if image:
    st.image(image, caption="Uploaded Image" if language == "English" else "আপলোড করা ছবি", width=400)

    if not st.session_state.messages:
        # First time processing this image
        st.info(analysis_text)

        # Location logic
        if gps_location and gps_location.get('latitude') is not None:
            lat = gps_location['latitude']
            lon = gps_location['longitude']
            city_name = get_precise_city(lat, lon)
            location = {"lat": lat, "lon": lon, "city": f"{city_name} (GPS)"}
        else:
            location = get_location()
            location["city"] = location["city"] + " (IP)"
        
        weather = get_weather(location["lat"], location["lon"])
        st.session_state.context = {"location": location, "weather": weather}

        # Build prompt & start chat
        prompt = build_prompt(weather, language)
        st.session_state.messages.append({"role": "user", "content": [{"image": image}, prompt]})
        
        advice = chat_with_agent(st.session_state.messages, language)
        st.session_state.messages.append({"role": "assistant", "content": advice})
        
        try:
            audio = text_to_speech(advice, lang=lang_key)
            st.session_state.audio = audio
        except Exception:
            st.session_state.audio = None

    # Always render context visually so it doesn't vanish on toggle
    if "context" in st.session_state:
        location = st.session_state.context["location"]
        weather = st.session_state.context["weather"]
        
        weather_desc = "বৃষ্টির সম্ভাবনা আছে" if weather['rain'] else "বৃষ্টির সম্ভাবনা নেই" 
        if language == "English":
            weather_desc = "Rain Expected" if weather['rain'] else "No Rain Expected"

        st.write(f"**{loc_prefix}** {location['city']}")
        st.write(f"**{weather_prefix}** {weather['temperature']}°C, {weather['humidity']}%, {weather_desc}")

    st.divider()

    # Display Chat History 
    #(Skip showing the first system prompt payload visually)
    for i, msg in enumerate(st.session_state.messages):
        if i == 0: continue # don't show the backend image+weather structure
        with st.chat_message(msg["role"]):
            content = msg["content"]
            if isinstance(content, list):
                for p in content:
                    if isinstance(p, dict) and "image" in p:
                        st.image(p["image"], width=300)
                    else:
                        st.write(p)
            else:
                st.write(content)

    # Play Audio of initial result
    if "audio" in st.session_state and st.session_state.audio:
        st.audio(st.session_state.audio)

    # Chat input for follow-ups
    chat_prompt = st.chat_input("Ask a follow up question / আরও কিছু জিজ্ঞাসা করুন...", accept_file=True)
    
    if chat_prompt:
        user_content = []
        # Multi-modal parsing (Streamlit 1.43+)
        if hasattr(chat_prompt, 'files') and chat_prompt.files:
            for file in chat_prompt.files:
                user_content.append({"image": file})
        
        text_part = chat_prompt.text if hasattr(chat_prompt, 'text') else str(chat_prompt) if isinstance(chat_prompt, str) else ""
        if text_part:
            user_content.append(text_part)

        st.session_state.messages.append({"role": "user", "content": user_content})

        # Show specific user chat message dynamically on bottom
        with st.chat_message("user"):
            for p in user_content:
                if isinstance(p, dict) and "image" in p:
                    st.image(p["image"], width=300)
                else:
                    st.write(p)
        
        # Get AI stream
        with st.chat_message("assistant"):
            st.info("Thinking..." if language == "English" else "ভাবছি...")
            ai_reply = chat_with_agent(st.session_state.messages, language)
            st.write(ai_reply)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
    # Handle pending translations instantly
    if "pending_translation" in st.session_state and st.session_state.pending_translation:
        with st.chat_message("assistant"):
            st.info("Translating into English..." if language == "English" else "বাংলায় অনুবাদ করা হচ্ছে...")
            ai_reply = chat_with_agent(st.session_state.messages, language)
            st.write(ai_reply)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
            try:
                audio = text_to_speech(ai_reply, lang=lang_key)
                st.session_state.audio = audio
            except Exception:
                pass
        
        del st.session_state.pending_translation
        st.rerun()

else:
    st.warning("দয়া করে একটি ছবি আপলোড করুন / Please upload an image" )