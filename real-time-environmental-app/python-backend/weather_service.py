"""
Standalone Python weather service for Kathmandu environmental monitoring.
This can be deployed separately and called from the Next.js frontend.
Run with: python weather_service.py
"""

import asyncio
import aiohttp
import json
from datetime import datetime
from collections import deque
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
KATHMANDU_LAT = 27.7172
KATHMANDU_LON = 85.3240
OPENMETEO_API_URL = "https://api.open-meteo.com/v1/forecast"
UPDATE_INTERVAL = 5  # seconds
HISTORY_SIZE = 120  # 10 minutes at 5-second intervals


class WeatherService:
    """Real-time weather data fetcher and storage."""
    
    def __init__(self):
        self.current_data: Dict[str, Any] = {}
        self.history: deque = deque(maxlen=HISTORY_SIZE)
        self.session: aiohttp.ClientSession | None = None
    
    async def initialize(self):
        """Initialize async session."""
        self.session = aiohttp.ClientSession()
    
    async def close(self):
        """Close async session."""
        if self.session:
            await self.session.close()
    
    async def fetch_weather_data(self) -> Dict[str, Any]:
        """Fetch current weather data from Open-Meteo API."""
        if not self.session:
            raise RuntimeError("Service not initialized. Call initialize() first.")
        
        params = {
            "latitude": KATHMANDU_LAT,
            "longitude": KATHMANDU_LON,
            "current": "temperature_2m,relative_humidity_2m,pressure_msl,weather_code",
            "hourly": "temperature_2m,relative_humidity_2m,pressure_msl",
            "timezone": "Asia/Kathmandu"
        }
        
        try:
            async with self.session.get(OPENMETEO_API_URL, params=params) as response:
                if response.status != 200:
                    raise Exception(f"API error: {response.status}")
                
                data = await response.json()
                
                self.current_data = {
                    "temperature": data["current"]["temperature_2m"],
                    "humidity": data["current"]["relative_humidity_2m"],
                    "pressure": data["current"]["pressure_msl"],
                    "weather_code": data["current"]["weather_code"],
                    "timestamp": datetime.now().isoformat(),
                }
                
                time_str = datetime.now().strftime("%H:%M:%S")
                self.history.append({
                    "timestamp": time_str,
                    "temperature": self.current_data["temperature"],
                    "humidity": self.current_data["humidity"],
                    "pressure": self.current_data["pressure"],
                })
                
                logger.info(f"Updated: {self.current_data['temperature']}°C, "
                          f"{self.current_data['humidity']}%, "
                          f"{self.current_data['pressure']} hPa")
                
                return {
                    "current": self.current_data,
                    "history": list(self.history),
                    "location": {
                        "latitude": KATHMANDU_LAT,
                        "longitude": KATHMANDU_LON,
                        "name": "Kathmandu, Nepal"
                    }
                }
        
        except Exception as e:
            logger.error(f"Error fetching weather data: {e}")
            raise
    
    async def start_continuous_updates(self):
        """Continuously fetch and store weather data."""
        logger.info("Starting continuous weather updates...")
        
        while True:
            try:
                await self.fetch_weather_data()
            except Exception as e:
                logger.error(f"Update cycle failed: {e}")
            
            await asyncio.sleep(UPDATE_INTERVAL)
    
    def get_current_data(self) -> Dict[str, Any]:
        """Get the latest weather data."""
        return self.current_data
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get historical weather data."""
        return list(self.history)


async def main():
    """Example: Run the weather service and print data periodically."""
    service = WeatherService()
    await service.initialize()
    
    try:
        # Start fetching in background
        fetch_task = asyncio.create_task(service.start_continuous_updates())
        
        # Print data every 10 seconds
        while True:
            await asyncio.sleep(10)
            current = service.get_current_data()
            if current:
                print(f"\n=== Weather Update ===")
                print(f"Temperature: {current['temperature']}°C")
                print(f"Humidity: {current['humidity']}%")
                print(f"Pressure: {current['pressure']} hPa")
                print(f"Updated: {current['timestamp']}")
    
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        await service.close()


if __name__ == "__main__":
    asyncio.run(main())
