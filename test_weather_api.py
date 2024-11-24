

from geopy.geocoders import Nominatim

from datetime import datetime
from meteostat import Daily, Point, Hourly
import pandas as pd

# Specify the city and state/province
city = "Toronto"
state = "Ontario"

geolocator = Nominatim(user_agent="geoapiWeatherDSGroupProj")

# Get the location by combining city and state
location = geolocator.geocode(f"{city}, {state}")

# Define the location (latitude, longitude, and elevation)
city = Point(location.latitude, location.longitude)  # Example: Toronto, Canada

# Define the date
start = datetime(2018, 1, 11, 0)
end = datetime(2018, 1, 11, 23)

# Fetch daily data
data = Hourly(city, start=start, end=end)
data = data.fetch()

print(data)

# Check if data is available
if not data.empty:
    # Extract weather code (if available)
    weather_code = data['coco'].iloc[0] if 'coco' in data else None
    
    # Interpret the weather code
    if weather_code is not None:
        if 0 <= weather_code <= 3:
            condition = "Clear"
        elif 45 <= weather_code <= 48:
            condition = "Fog"
        elif 51 <= weather_code <= 57:
            condition = "Drizzle"
        elif 61 <= weather_code <= 67:
            condition = "Rain"
        elif 71 <= weather_code <= 77:
            condition = "Snow"
        elif 80 <= weather_code <= 82:
            condition = "Rain Showers"
        elif 85 <= weather_code <= 86:
            condition = "Snow Showers"
        elif 95 <= weather_code <= 99:
            condition = "Thunderstorm"
        else:
            condition = "Unknown"
        print(f"Weather on {start}: {condition}")
    else:
        print(f"No weather condition code available for {start}.")
else:
    print(f"No data available for {start}.")
