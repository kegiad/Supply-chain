import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('TOMORROW_API_KEY')

base_url = 'https://api.tomorrow.io/v4/timelines'

latitude = 9.917542
longitude = 76.780557

params = {
    'apikey': api_key,
    'location': f'{latitude},{longitude}',
    'fields': 'temperature,precipitationProbability',
    'timesteps': 'current',
    'units': 'metric',
}

response = requests.get(base_url, params=params)

if response.status_code == 200:
    weather_data = response.json()
    print("Weather Data:", weather_data)
else:
    print(f"Error: {response.status_code}, {response.text}")