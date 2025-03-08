from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class PropertyData(BaseModel):
    """Schema for property data extraction"""
    building_name: str = Field(description="Name of the building/property", alias="Building_name")
    property_type: str = Field(description="Type of property (commercial, residential, etc)", alias="Property_type")
    location_address: str = Field(description="Complete address of the property")
    price: str = Field(description="Price of the property", alias="Price")
    description: str = Field(description="Detailed description of the property", alias="Description")
    url: Optional[str] = Field(description="URL of the property listing", default=None)
    area_sqft: Optional[float] = Field(description="Area of the plot in square feet", default=None)
    dimensions: Optional[str] = Field(description="Dimensions of the plot (length x width)", default=None)
    approved_for_construction: Optional[bool] = Field(description="Whether the plot is approved for construction", default=None)

class PropertiesResponse(BaseModel):
    """Schema for multiple properties response"""
    properties: List[PropertyData] = Field(description="List of property details")

class LocationData(BaseModel):
    """Schema for location price trends"""
    location: str
    price_per_sqft: float
    percent_increase: float
    rental_yield: float

class LocationsResponse(BaseModel):
    """Schema for multiple locations response"""
    locations: List[LocationData] = Field(description="List of location data points")

class FirecrawlResponse(BaseModel):
    """Schema for Firecrawl API response"""
    success: bool
    data: Dict
    status: str
    expiresAt: str

class PropertyLocation(BaseModel):
    """Schema for property location data"""
    property_id: str
    property_name: str
    address: str
    latitude: float
    longitude: float
    price: str
    url: Optional[str] = None
