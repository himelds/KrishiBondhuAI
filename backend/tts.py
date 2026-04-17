from gtts import gTTS
import re

def clean_text_for_speech(text):
    # Remove markdown bold/italic asterisks and underscores
    text = re.sub(r'[*_]{1,3}', '', text)
    # Remove markdown headers
    text = re.sub(r'#+\s*', '', text)
    # Remove colons, dashes, and greater than signs
    text = re.sub(r'[:\->]', ' ', text)
    return text

def text_to_speech(text, lang='bn'):
    clean_text = clean_text_for_speech(text)
    tts = gTTS(text=clean_text, lang=lang)
    tts.save("output.mp3")
    return "output.mp3"