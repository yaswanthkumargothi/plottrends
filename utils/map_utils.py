import folium
from typing import List, Tuple
from models.schemas import PropertyLocation
from agents.mapping_agent import LocationMappingAgent
import os

def create_map_with_properties(property_locations: List[PropertyLocation], city: str):
    """Create a folium map with property markers"""
    # Calculate the average lat and lon to center the map
    if not property_locations:
        # Default to city center (will be obtained via geocoding)
        map_center = LocationMappingAgent(os.getenv('OPENAI_API_KEY')).geocode_address("", city)
    else:
        valid_locations = [(loc.latitude, loc.longitude) for loc in property_locations 
                            if loc.latitude != 0.0 and loc.longitude != 0.0]
        if valid_locations:
            lat_sum = sum(lat for lat, _ in valid_locations)
            lon_sum = sum(lon for _, lon in valid_locations)
            map_center = (lat_sum / len(valid_locations), lon_sum / len(valid_locations))
        else:
            map_center = LocationMappingAgent(os.getenv('OPENAI_API_KEY')).geocode_address("", city)
    
    # Create map
    m = folium.Map(location=map_center, zoom_start=12)
    
    # Add markers for each property
    for loc in property_locations:
        if loc.latitude == 0.0 and loc.longitude == 0.0:
            continue  # Skip properties with invalid coordinates
            
        # Create popup content
        popup_html = f"""
        <div style="width:250px">
            <h4>{loc.property_name}</h4>
            <p><b>Price:</b> {loc.price}</p>
            <p><b>Address:</b> {loc.address}</p>
            <p><a href="{loc.url}" target="_blank">View Property</a></p>
        </div>
        """
        
        folium.Marker(
            location=[loc.latitude, loc.longitude],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{loc.property_name} - {loc.price}",
            icon=folium.Icon(color="blue", icon="home")
        ).add_to(m)
    
    return m
