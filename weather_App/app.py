from flask import Flask, render_template, jsonify
from flask_cors import CORS
import asyncio
import aiohttp
import threading
from datetime import datetime
from collections import deque
import json

app = Flask(__name__)
CORS(app)

# Configuration
KATHMANDU_LAT = 27.7172
KATHMANDU_LON = 85.3240
API_URL = "https://api.open-meteo.com/v1/forecast"
REFRESH_INTERVAL = 5  # seconds
MAX_DATA_POINTS = 120  # Keep 10 minutes of data (120 * 5 seconds)

# Data storage
data_storage = {
    'timestamps': deque(maxlen=MAX_DATA_POINTS),
    'temperature': deque(maxlen=MAX_DATA_POINTS),
    'humidity': deque(maxlen=MAX_DATA_POINTS),
    'pressure': deque(maxlen=MAX_DATA_POINTS),
    'current': {
        'temperature': None,
        'humidity': None,
        'pressure': None,
        'weather_code': None,
        'timestamp': None
    }
}

async def fetch_weather_data():
    """Fetch current weather data from Open-Meteo API"""
    params = {
        'latitude': KATHMANDU_LAT,
        'longitude': KATHMANDU_LON,
        'current': 'temperature_2m,relative_humidity_2m,pressure_msl,weather_code',
        'timezone': 'Asia/Kathmandu'
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('current', {})
                else:
                    print(f"API Error: Status {response.status}")
                    return None
    except Exception as e:
        print(f"Error fetching weather data: {str(e)}")
        return None

def get_weather_description(code):
    """Convert WMO weather code to description"""
    weather_codes = {
        0: 'Clear sky',
        1: 'Mainly clear',
        2: 'Partly cloudy',
        3: 'Overcast',
        45: 'Foggy',
        48: 'Foggy',
        51: 'Light drizzle',
        53: 'Moderate drizzle',
        55: 'Dense drizzle',
        61: 'Slight rain',
        63: 'Moderate rain',
        65: 'Heavy rain',
        71: 'Slight snow',
        73: 'Moderate snow',
        75: 'Heavy snow',
        80: 'Slight rain showers',
        81: 'Moderate rain showers',
        82: 'Violent rain showers',
        85: 'Slight snow showers',
        86: 'Heavy snow showers',
        95: 'Thunderstorm',
        96: 'Thunderstorm with hail',
        99: 'Thunderstorm with hail'
    }
    return weather_codes.get(code, 'Unknown')

async def periodic_data_fetch():
    """Periodically fetch weather data and update storage"""
    while True:
        try:
            await asyncio.sleep(REFRESH_INTERVAL)
            current_data = await fetch_weather_data()
            
            if current_data:
                timestamp = datetime.now().strftime('%H:%M:%S')
                temp = current_data.get('temperature_2m')
                humidity = current_data.get('relative_humidity_2m')
                pressure = current_data.get('pressure_msl')
                
                # Update current data
                data_storage['current']['temperature'] = temp
                data_storage['current']['humidity'] = humidity
                data_storage['current']['pressure'] = pressure
                data_storage['current']['weather_code'] = current_data.get('weather_code')
                data_storage['current']['timestamp'] = timestamp
                
                # Add to historical data
                data_storage['timestamps'].append(timestamp)
                data_storage['temperature'].append(temp)
                data_storage['humidity'].append(humidity)
                data_storage['pressure'].append(pressure)
                
                print(f"[{timestamp}] Updated - Temp: {temp}°C, Humidity: {humidity}%, Pressure: {pressure} hPa")
        
        except Exception as e:
            print(f"Error in periodic fetch: {str(e)}")

def start_background_fetch():
    """Start the background data fetching in a separate thread"""
    def run_async_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(periodic_data_fetch())
    
    thread = threading.Thread(target=run_async_loop, daemon=True)
    thread.start()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/api/current')
def get_current():
    """API endpoint for current weather data"""
    return jsonify(data_storage['current'])

@app.route('/api/history')
def get_history():
    """API endpoint for historical data"""
    return jsonify({
        'timestamps': list(data_storage['timestamps']),
        'temperature': list(data_storage['temperature']),
        'humidity': list(data_storage['humidity']),
        'pressure': list(data_storage['pressure'])
    })

@app.route('/api/weather-description')
def get_weather_info():
    """API endpoint for weather description"""
    code = data_storage['current'].get('weather_code')
    description = get_weather_description(code) if code else 'N/A'
    return jsonify({'description': description, 'code': code})

if __name__ == '__main__':
    # Start background data fetching
    start_background_fetch()
    # Run Flask app
    app.run(debug=True, use_reloader=False, port=5000)
