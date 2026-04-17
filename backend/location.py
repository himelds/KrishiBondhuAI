import requests

def get_location():
    try:
        response = requests.get('https://ipapi.co/json/', timeout=5)
        data = response.json()
        return {
            "lat": data.get("latitude", 23.8103),  # Default to Dhaka, Bangladesh on fail
            "lon": data.get("longitude", 90.4125),
            "city": data.get("city", "Unknown City")
        }
    except Exception:
        # Fallback to Dhaka
        return {
            "lat": 23.8103,
            "lon": 90.4125,
            "city": "Dhaka (Fallback)"
        }

def get_precise_city(lat, lon):
    try:
        url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lon}&localityLanguage=bn"
        response = requests.get(url, timeout=5)
        data = response.json()
        city = data.get("city") or data.get("locality") or data.get("principalSubdivision") or "Unknown Precise Location"
        return city
    except Exception:
        return "Unknown Location"