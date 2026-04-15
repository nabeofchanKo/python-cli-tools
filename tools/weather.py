import requests
import argparse

CITIES = {
      "Tokyo": (35.6762, 139.6503),
      "Osaka": (34.6937, 135.5023),
      "Singapore": (1.3521, 103.8198),
      "London": (51.5074, -0.1278),
      "New York": (40.7128, -74.0060),
  }

WEATHER_CODES = {
      0: "Clear sky",
      1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
      45: "Fog", 48: "Depositing rime fog",
      51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
      61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
      71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
      80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
      95: "Thunderstorm",
  }

def fetch_weather(lat: float, lon: float) -> dict:
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=Asia/Tokyo"
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException:
        print("Error: Could not connect to the weather API")
        return
    
    if response.status_code != 200:
        print(f"Error: API returned status code {response.status_code}")
        return
    
    return response.json()

def format_output(city: str, data: dict) -> str:
    current_weather = data["current_weather"]
    temperature = current_weather["temperature"]
    windspeed = current_weather["windspeed"]
    weathercode = current_weather["weathercode"]
    time = current_weather["time"]
    time = time.replace("T", " ")

    condition = WEATHER_CODES.get(weathercode)
    if condition is None:
        condition = f"Unknown weather code: {weathercode}"

    res = \
        f"=== Weather in {city} ===\n" + \
        f"Time: {time}\n" + \
        f"Temperature: {temperature}°C\n" + \
        f"Wind Speed: {windspeed} km/h\n"  + \
        f"Condition: {condition}\n"
    
    return res

def main():
    # argparse
    parser = argparse.ArgumentParser(description="Weather information")
    parser.add_argument("city", help="Select a city for weather information")
    args = parser.parse_args()
    
    # Format city
    city = args.city.title()

    # Get Latitude and Longtitude
    coords = CITIES.get(city)
    if coords is None:
        print(f"Error: Unknown city '{city}'")
        return
    else:
        lat, lon = coords
    
    data = fetch_weather(lat, lon)
    if data is not None:
        text = format_output(city, data)
        print(text)



if __name__ == "__main__":
    main()