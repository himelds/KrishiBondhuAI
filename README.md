# 🌾 KrishiBondhu AI  
### Bangla Multimodal Farming Assistant powered by Gemma
🚀 Built for the Gemma 4 Good Hackathon (Kaggle)

---

## 📌 Overview

**KrishiBondhu AI** is an intelligent, multimodal agricultural assistant designed to support Bangla-speaking farmers with:

- 📸 Crop disease detection  
- 🌦️ Weather-aware spray recommendations  
- ⚠️ Disease risk alerts  
- 🔊 Bangla voice guidance  

Our system combines **computer vision + real-time weather + AI reasoning** to deliver **simple, actionable advice in Bangla**.

---

## 🎯 Problem Statement

Farmers in Bangladesh often face:

- Limited access to agricultural experts  
- Difficulty understanding technical recommendations  
- Poor timing of pesticide/fertilizer application  
- Lack of localized, real-time guidance  

👉 This leads to crop loss, increased costs, and reduced productivity.

---

## 💡 Our Solution

KrishiBondhu AI provides:

- ✅ Instant disease detection from crop images  
- ✅ Smart spray timing advice based on weather  
- ✅ Easy-to-understand Bangla explanations  
- ✅ Voice output for accessibility  

---

## 🧠 Core Innovation

At the heart of our system is **Gemma**, used as a reasoning engine.

Instead of just predicting, we:

> 🔥 Combine disease + weather + context → Generate intelligent farming decisions

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER Upoload Image                       │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (Streamlit)                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     BACKEND API (Python)                    │
└────────┬────────────────┼─────────────────┬─────────────────┘
         │                │                 │
         ▼                ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Weather    │  │    Image     │  │   Location   │
│   Data API   │  │              │  │  Detection   │
└──────────────┘  └──────────────┘  └──────────────┘
         │                │                 │
         └────────────────┼─────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│               Data Aggregation Layer                        │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              🤖 Gemma AI (Reasoning Engine)                 │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌──────────────────────────┼─────────────────┐
          ▼                          ▼                 ▼
┌───────────────────────┐     ┌──────────────┐  ┌──────────────┐
│    Disease name       │     │     Spray    │  │ Risk warning │
│Explanation, Treatment │     │   Decision   │  │              │
└───────────────────────┘     └──────────────┘  └──────────────┘
```

---

## 🔄 End-to-End Workflow

1. 📸 Farmer uploads crop image  
2. 🧠 Disease detection model identifies issue  
3. 📍 System detects location  
4. 🌦️ Weather data is fetched  
5. 🤖 Gemma processes all inputs  
6. 📢 Outputs:
   - Disease explanation (Bangla)  
   - Treatment advice  
   - Spray timing decision  
   - Risk warning  
7. 🔊 Text converted to Bangla speech  

---

## 🧩 Features

### 📸 Disease Detection
- Input: Leaf image  
- Output: Disease name + confidence  

### 🌧️ Spray Timing Advisor
- Uses weather conditions  
- Recommends: Spray now ❌ / Delay ✅  

### ⚠️ Disease Risk Warning
- Based on humidity + temperature  

### 📍 Auto Location Detection
- Uses IP/GPS to fetch local weather  

### 🔊 Bangla Voice Output
- Converts AI advice into speech  

---

## 🛠️ Tech Stack

| Component   | Technology             |
|-------------|------------------------|
| Frontend    | Streamlit              |
| Backend     | Python                 |
| AI Model    | Gemma                  |
| CV Model    | MobileNet / EfficientNet |
| Weather API | OpenWeather            |
| TTS         | gTTS                   |

---

## 📂 Project Structure

```
krishibondhu-ai/
│
├── app.py                  # Frontend (Streamlit)
│
├── backend/
│   ├── weather.py          # Weather API integration
│   ├── location.py         # Location detection
│   ├── gemma.py            # AI reasoning engine
│   └── tts.py              # Text-to-speech (Bangla)
│
└── requirements.txt        # Python dependencies
```

---

## ⚙️ Setup Instructions (IMPORTANT)

Follow these steps carefully 👇

1. Clone the repository:

```bash
git clone https://github.com/himelds/KrishiBondhuAI.git
cd krishibondhu-ai
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run app.py
```

---

## 👥 Contributors

<table>
  <tr>
    <td align="center">
      <b>Himel Das</b>
    </td>
    <td align="center">
      <b>Shuva Palit</b>
    </td>
    <td align="center">
      <b>Trisha Das</b>
    </td>
  </tr>
</table>

---

> Made with ❤️ for the farmers of Bangladesh
