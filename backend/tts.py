from gtts import gTTS

def text_to_speech(text):
    tts = gTTS(text=text, lang='bn')
    tts.save("output.mp3")
    return "output.mp3"