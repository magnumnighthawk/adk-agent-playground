import os
from dotenv import load_dotenv
from httpx import request
import googlemaps
from google.adk.agents.llm_agent import Agent
from .instructions import WEATHER_ASSISTANT_INSTRUCTION

load_dotenv()
gmp_key = os.getenv('GMP_API_KEY')
user_location = os.getenv('USER_LOCATION', 'Manchester, Greater Manchester')
gmaps = googlemaps.Client(key=gmp_key)

def get_user_location() -> dict:
    """
    Fetches the user's current location details using Google Maps Geocoding API.

    Returns:
        dict: A dictionary containing location details such as city, country, pincode, administrative zones, and coordinates.
            - address_components: {
                long_name: string;
                short_name: string;
                types: string[];
            }[];
            - formatted_address: string;
            - geometry: dict;

    Example:
    [
        {
            address_components: [
            {
                long_name: "Manchester",
                short_name: "Manchester",
                types: ["locality", "political"],
            },
            {
                long_name: "Greater Manchester",
                short_name: "Greater Manchester",
                types: ["administrative_area_level_2", "political"],
            },
            {
                long_name: "England",
                short_name: "England",
                types: ["administrative_area_level_1", "political"],
            },
            {
                long_name: "United Kingdom",
                short_name: "GB",
                types: ["country", "political"],
            },
            {
                long_name: "M1",
                short_name: "M1",
                types: ["postal_code", "postal_code_prefix"],
            },
            ],
            formatted_address: "Manchester M1, UK",
            geometry: {
                bounds: {
                    northeast: { lat: 53.5151, lng: -2.2084 },
                    southwest: { lat: 53.4325, lng: -2.3073 },
                },
                location: { lat: 53.4808, lng: -2.2426 },
                location_type: "APPROXIMATE",
                viewport: {
                    northeast: { lat: 53.5151, lng: -2.2084 },
                    southwest: { lat: 53.4325, lng: -2.3073 },
                },
                },
            place_id: "ChIJ2_UmUkGxe0gRvCRBcg0hXQg",
            types: ["locality", "political"],
        },
        ];
    """
    response = gmaps.geocode(user_location)
    if response:
        return { 'status': 'success', 'data': response }
    
def get_current_weather(coordinates: dict) -> dict:
    """
    Fetches ONLY the current moment's weather conditions for the given coordinates.
    This tool also provides the current time at the location.
    
    Use this tool when the user asks about:
    - Current weather right now
    - What's the weather like at this moment
    - Temperature right now
    - Current time or what time it is
    
    DO NOT use this tool when the user asks about:
    - Daily forecasts
    - Weather for tomorrow or future days
    - Sunrise/sunset times
    - Full day weather overview
    
    Args:
        coordinates (dict): A dictionary containing latitude and longitude.
            - lat: float
            - lng: float
    Returns:
        dict: A dictionary containing current weather conditions including temperature, humidity, wind speed, weather description, and current time.
    """
    response = request(
        "GET",
        "https://weather.googleapis.com/v1/currentConditions:lookup",
        params={
            "key": gmp_key, "location.latitude": coordinates.get("lat"), "location.longitude": coordinates.get("lng")})
    if response.status_code == 200:
        return { 'status': 'success', 'data': response.json() }

def get_daily_forecast(coordinates: dict, days: int = 1) -> dict:
    """
    Fetches daily weather forecast including daytime, nighttime conditions, sunrise, and sunset times.
    
    Use this tool when the user asks about:
    - Daily weather forecast
    - Weather for tomorrow or specific future days
    - Sunrise/sunset times
    - Full day weather overview (daytime and nighttime)
    - Multi-day forecasts
    - Planning activities based on weather
    
    DO NOT use this tool when the user only asks about current weather conditions right now.
    
    Args:
        coordinates (dict): A dictionary containing latitude and longitude.
            - lat: float
            - lng: float
        days (int): Number of days to forecast (default: 1, max: 10)
    Returns:
        dict: A dictionary containing daily forecasts with:
            - Daily temperature highs and lows
            - Daytime and nighttime conditions
            - Sunrise and sunset times
            - Precipitation probability
            - Weather descriptions for each day
    """
    response = request(
        "GET",
        "https://weather.googleapis.com/v1/forecast/days:lookup",
        params={
            "key": gmp_key, 
            "location.latitude": coordinates.get("lat"), 
            "location.longitude": coordinates.get("lng"),
            "days": days
        })
    if response.status_code == 200:
        return { 'status': 'success', 'data': response.json() }

root_agent = Agent(
    model='gemini-2.0-flash',
    name='expert_weather_assistant',
    description='A helpful assistant that provides weather information to the user.',
    instruction=WEATHER_ASSISTANT_INSTRUCTION,
    tools=[get_user_location, get_current_weather, get_daily_forecast]
)
