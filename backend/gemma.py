from PIL import Image
import io

def build_prompt(weather):
    return f"""
You are an agricultural assistant for Bangladeshi farmers.

Analyze the crop image and identify the disease.

Then:
1. Name the disease
2. Explain in simple Bangla
3. Give treatment advice
4. Decide if spraying pesticide/fertilizer is appropriate
5. Explain based on weather
6. Give risk warning

Weather:
- Rain: {"Yes" if weather["rain"] else "No"}
- Humidity: {weather["humidity"]}%
- Temperature: {weather["temperature"]}°C

Answer in simple Bangla.

Format:
রোগ:
চিকিৎসা:
পরামর্শ:
সতর্কতা:
"""

def get_advice(data):
    image_file = data["image"]
    weather = data["weather"]

    # Convert uploaded file to PIL Image
    image = Image.open(io.BytesIO(image_file.read()))

    # Build prompt
    prompt = build_prompt(weather)

    # 🔴 TEMPORARY (since real Gemma multimodal not connected yet)
    # This is just to keep system running
    response = f"""
রোগ:
পাতায় দাগ দেখা যাচ্ছে (সম্ভাব্য রোগ)

চিকিৎসা:
উপযুক্ত ছত্রাকনাশক ব্যবহার করুন।

পরামর্শ:
{"এখন স্প্রে করবেন না (বৃষ্টি আসছে)" if weather["rain"] else "এখন স্প্রে করা যেতে পারে"}

সতর্কতা:
উচ্চ আর্দ্রতায় রোগ দ্রুত ছড়াতে পারে।
"""

    return response