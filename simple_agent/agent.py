import os
from dotenv import load_dotenv
from httpx import request
import googlemaps
from google.adk.agents.llm_agent import Agent
from .instructions import WEATHER_ASSISTANT_INSTRUCTION

load_dotenv()
gmp_key = os.getenv('GMP_API_KEY')
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
    # Fetch user's current location and details like city, country, pincode, administrative zones & coordinates using Google Maps Geocoding API
    response = gmaps.geocode('Manchester, Greater Manchester')
    if response:
        return { 'status': 'success', 'data': response }
    
def get_weather(coordinates: dict) -> dict:
    """
    Fetches the current weather information for the given coordinates using Google Weather API.
    Args:
        coordinates (dict): A dictionary containing latitude and longitude.
            - lat: float
            - lng: float
    Returns:
        dict: A dictionary containing current weather conditions including temperature, humidity, wind speed, and weather description.
    """
    # Fetch weather information for the given coordinates using Google Weather API
    # Returns current weather conditions including temperature, humidity, wind speed, and weather description
    response = request(
        "GET",
        "https://weather.googleapis.com/v1/currentConditions:lookup",
        params={
            "key": gmp_key, "location.latitude": coordinates.get("lat"), "location.longitude": coordinates.get("lng")})
    if response.status_code == 200:
        return { 'status': 'success', 'data': response.json() }

root_agent = Agent(
    model='gemini-2.0-flash',
    name='expert_weather_assistant',
    description='A helpful assistant that provides weather information to the user.',
    instruction=WEATHER_ASSISTANT_INSTRUCTION,
    tools=[get_user_location, get_weather]
)
