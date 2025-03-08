from typing import List, Tuple
from agno.agent import Agent
from agno.models.openai import OpenAIChat
import requests
import json
import time
from models.schemas import PropertyLocation

class LocationMappingAgent:
    """Agent responsible for geocoding property addresses and preparing map data"""
    
    def __init__(self, openai_api_key: str, model_id: str = "o3-mini"):
        self.agent = Agent(
            model=OpenAIChat(id=model_id, api_key=openai_api_key),
            markdown=True,
            description="I am a geolocation expert who converts addresses to coordinates and prepares map data."
        )
        # Using Nominatim geocoding service
        self.geocoding_url = "https://nominatim.openstreetmap.org/search"
    
    def geocode_address(self, address: str, city: str) -> Tuple[float, float]:
        """Convert address to latitude and longitude using Nominatim"""
        full_address = f"{address}, {city}"
        
        params = {
            'q': full_address,
            'format': 'json',
            'limit': 1
        }
        
        headers = {
            'User-Agent': 'PlotTrends/1.0'
        }
        
        try:
            response = requests.get(self.geocoding_url, params=params, headers=headers)
            data = response.json()
            
            if data and len(data) > 0:
                return float(data[0]['lat']), float(data[0]['lon'])
            else:
                # Fall back to city coordinates if specific address not found
                city_params = {'q': city, 'format': 'json', 'limit': 1}
                city_response = requests.get(self.geocoding_url, params=city_params, headers=headers)
                city_data = city_response.json()
                
                if city_data and len(city_data) > 0:
                    return float(city_data[0]['lat']), float(city_data[0]['lon'])
                
                # Default coordinates if geocoding fails completely
                return 0.0, 0.0
        except Exception as e:
            print(f"Geocoding error: {e}")
            return 0.0, 0.0
    
    def process_properties(self, properties: List[dict], city: str) -> List[PropertyLocation]:
        """Process properties and get their geographic coordinates"""
        property_locations = []
        
        for idx, prop in enumerate(properties):
            address = prop.get('location_address', '')
            property_name = prop.get('building_name', f"Plot {idx+1}")
            price = prop.get('price', 'Price not available')
            url = prop.get('url', '')
            
            # Allow time for API rate limiting
            if idx > 0:
                time.sleep(1)  # Be respectful to the geocoding API
            
            lat, lon = self.geocode_address(address, city)
            
            property_locations.append(
                PropertyLocation(
                    property_id=f"prop_{idx}",
                    property_name=property_name,
                    address=address,
                    latitude=lat,
                    longitude=lon,
                    price=price,
                    url=url
                )
            )
        
        return property_locations
    
    def generate_area_insights(self, property_locations: List[PropertyLocation], city: str) -> str:
        """Generate insights about the geographic distribution of properties"""
        if not property_locations:
            return "No property location data available for analysis."
        
        # Convert to JSON for the agent
        locations_json = json.dumps([loc.dict() for loc in property_locations])
        
        analysis = self.agent.run(
            f"""As a geolocation and real estate expert, analyze the geographic distribution of these plots in {city}:

            {locations_json}

            Please provide:
            
            1. GEOGRAPHIC DISTRIBUTION ANALYSIS
               - Analyze how the properties are distributed across the city
               - Identify clusters or patterns in the locations
               - Comment on the relationship between location and price
            
            2. PROXIMITY ANALYSIS
               - For each property, identify nearby amenities or landmarks
               - Analyze accessibility to major roads, public transport
               - Evaluate the overall connectivity score for each location
            
            3. DEVELOPMENT TRAJECTORY
               - Based on the locations, predict future development directions in the city
               - Identify emerging areas versus established locations
               - Suggest which areas show highest development potential
               
            Format your response in a clear, structured way using bullet points and sections.
            """
        )
        
        return analysis.content
