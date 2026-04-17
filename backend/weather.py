import requests

def get_weather(lat, lon):
    try:
        # Using Open-Meteo for free weather data (no API key required)
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation&timezone=auto"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        current = data.get("current", {})
        
        return {
            "rain": current.get("precipitation", 0) > 0,
            "humidity": current.get("relative_humidity_2m", 80),
            "temperature": current.get("temperature_2m", 30)
        }
    except Exception:
        # Fallback to a default hot/humid weather if API fails
        return {
            "rain": False,
            "humidity": 85,
            "temperature": 32
        }