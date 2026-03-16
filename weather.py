import requests

API_KEY = "51c240ffaa7ab718422d70bfb71fc841"  # replace with your key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    try:
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200 and "weather" in data:
            # Return main condition like 'Sunny', 'Rain', 'Cloudy'
            return {"condition": data["weather"][0]["main"]}
        else:
            return {"condition": "Unknown"}

    except Exception as e:
        print("Error fetching weather:", e)
        return {"condition": "Unknown"}