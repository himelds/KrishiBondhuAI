import os
from PIL import Image
import io
from google import genai
from google.genai import types

def build_prompt(weather, language):
    lang_instruction = "Answer strictly in English." if language == "English" else "Answer strictly in simple Bangla."
    
    format_instruction = """
Format:
Disease: 
Treatment: 
Advice: 
Warning: 
""" if language == "English" else """
Format:
রোগ:
চিকিৎসা:
পরামর্শ:
সতর্কতা:
"""

    return f"""
You are an agricultural assistant for farmers.

Analyze the crop image and identify the disease.

Then:
1. Name the disease
2. Explain it simply
3. Give treatment advice
4. Decide if spraying pesticide/fertilizer is appropriate based on weather
5. Give risk warning

Weather Context:
- Rain: {"Yes" if weather["rain"] else "No"}
- Humidity: {weather["humidity"]}%
- Temperature: {weather["temperature"]}°C

{lang_instruction}
{format_instruction}
"""

def chat_with_agent(messages_ui, language):
    client = genai.Client()
    
    # Enforcer string to prevent language drift
    enforcer = "\n\n[Reply strictly in English.]" if language == "English" else "\n\n[অবশ্যই বাংলা ভাষায় উত্তর দিন।]"
    
    # Convert Streamlit dictionary messages to GenAI Content objects
    contents = []
    for i, msg in enumerate(messages_ui):
        role = "user" if msg["role"] == "user" else "model"
        parts = msg["content"]
        
        is_last_message = (i == len(messages_ui) - 1)
        
        if isinstance(parts, list):
            genai_parts = []
            for p in parts:
                if isinstance(p, dict) and "image" in p:
                    image_file = p["image"]
                    img = Image.open(io.BytesIO(image_file.read()))
                    image_file.seek(0) # Reset pointer
                    
                    img_byte_arr = io.BytesIO()
                    # Convert to RGB to prevent transparency saving errors in JPEG
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    img.save(img_byte_arr, format='JPEG')
                    image_bytes = img_byte_arr.getvalue()
                    
                    genai_parts.append(types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"))
                else:
                    text_str = str(p)
                    if is_last_message and role == "user":
                        text_str += enforcer
                    genai_parts.append(types.Part.from_text(text=text_str))
            contents.append(types.Content(role=role, parts=genai_parts))
        else:
            text_str = str(parts)
            if is_last_message and role == "user":
                text_str += enforcer
            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=text_str)]))

    try:
        response = client.models.generate_content(
            model='gemma-4-31b-it',
            contents=contents,
        )
        return response.text
    except Exception as e:
        return f"Error / ত্রুটি: {str(e)}"