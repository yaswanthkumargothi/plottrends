from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from firecrawl import FirecrawlApp
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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

class PropertyFindingAgent:
    """Agent responsible for finding properties and providing recommendations"""
    
    def __init__(self, firecrawl_api_key: str, openai_api_key: str, model_id: str = "o3-mini"):
        self.agent = Agent(
            model=OpenAIChat(id=model_id, api_key=openai_api_key),
            markdown=True,
            description="I am a real estate expert who helps find and analyze properties based on user preferences."
        )
        self.firecrawl = FirecrawlApp(api_key=firecrawl_api_key)

    def find_properties(
        self, 
        city: str,
        max_price: float,
        property_category: str = "Residential",
        property_type: str = "Plot"
    ) -> str:
        """Find and analyze properties based on user preferences"""
        formatted_location = city.lower()
        
        urls = [
            f"https://www.squareyards.com/sale/plot-for-sale-in-{formatted_location}/*",
            f"https://www.99acres.com/plots-in-{formatted_location}-ffid/*",
            f"https://housing.com/in/buy/plots/{formatted_location}/{formatted_location}",
            f"https://www.magicbricks.com/property-for-sale/residential-plot/{formatted_location}-all/*",
        ]
        
        raw_response = self.firecrawl.extract(
            urls=urls,
            params={
                'prompt': f"""Extract ONLY 10 OR LESS different {property_category} Plots from {city} that cost less than {max_price} crores.
                
                Requirements:
                - Property Category: {property_category} plots only
                - Property Type: Plot/Land only
                - Location: {city}
                - Maximum Price: {max_price} crores
                - Include complete plot details with exact location
                - IMPORTANT: Extract specific plot details including:
                  - Plot area in square feet
                  - Plot dimensions where available
                  - Legal approvals status
                  - GATED or OPEN plot
                  - Connectivity details
                  - Nearby landmarks and facilities
                - IMPORTANT: Include the original property URL for each listing
                - Return data for at least 5 different plots. MAXIMUM 10.
                - Format as a list of plots with their respective details
                """,
                'schema': PropertiesResponse.model_json_schema()
            }
        )
        
        print("Raw Property Response:", raw_response)
        
        if isinstance(raw_response, dict) and raw_response.get('success'):
            properties = raw_response['data'].get('properties', [])
        else:
            properties = []
            
        print("Processed Properties:", properties)

        
        analysis = self.agent.run(
            f"""As a real estate expert, analyze these plots and market trends:

            Properties Found in json format:
            {properties}

            **IMPORTANT INSTRUCTIONS:**
            1. ONLY analyze plots from the above JSON data that match the user's requirements:
               - Property Category: {property_category}
               - Maximum Price: {max_price} crores
            2. From the matching plots, select the 5 best plots

            Please provide your analysis in this format:
            
            First, for each of the 5 best plots, create an HTML div with class="property-card" that contains the property details.
            DO NOT wrap this HTML in triple backticks or markdown code blocks.
            START EACH CARD with <div class="property-card" and END with </div>
            
            Then, AFTER ALL HTML CARDS, start a new section with "---ANALYSIS_SECTION_BELOW---" followed by your analysis text.

            Your analysis should include:

            💰 PLOT VALUE ANALYSIS
            • Compare the selected plots based on:
              - Price per sq ft
              - Location advantage
              - Development potential
              - Legal clearances
              - Future appreciation potential

            📍 LOCATION INSIGHTS FOR PLOT INVESTMENT
            • Specific advantages of investing in plots in these areas
            • Infrastructure development plans
            • Growth trajectory of the area

            💡 INVESTMENT RECOMMENDATIONS
            • Top 3 plots from the selection with reasoning
            • Expected ROI timeline
            • Development possibilities
            • Points to consider before purchase

            🤝 NEGOTIATION TIPS FOR PLOT PURCHASES
            • Plot-specific negotiation strategies
            • Documentation verification checklist
            • Legal considerations specific to land purchases

            Remember: First provide ALL HTML cards without code blocks, then the text analysis AFTER the marker.
            """
        )
        
        return analysis.content

    def get_location_trends(self, city: str) -> str:
        """Get price trends for different localities in the city"""
        raw_response = self.firecrawl.extract([
            f"https://www.99acres.com/property-rates-and-price-trends-in-{city.lower()}-prffid/*",
            f"https://housing.com/in/buy/plots/{city.lower()}/{city.lower()}"
        ], {
            'prompt': f"""Extract price trends data for ALL major localities in {city} SPECIFICALLY FOR PLOTS/LAND.
            
            IMPORTANT: 
            - Focus on PLOT/LAND prices, not apartments or houses
            - Return data for at least 5-10 different localities
            - Include both premium and affordable areas
            - Extract the following for each locality:
              * Current price per sq ft for plots
              * Year-on-year appreciation percentage
              * Future growth potential
              * Infrastructure development status
              * Connectivity details
            - Format as a list of locations with their respective data
            """,
            'schema': LocationsResponse.model_json_schema(),
        })
        
        if isinstance(raw_response, dict) and raw_response.get('success'):
            locations = raw_response['data'].get('locations', [])
    
            analysis = self.agent.run(
                f"""As a real estate expert specializing in plot investments, analyze these location price trends for {city}:

                {locations}

                Please provide:
                1. A bullet-point analysis of plot price trends for each location with focus on:
                   - Current price per sq ft
                   - Historical appreciation rates
                   - Future growth potential
                
                2. Identify the top 3 locations for plot investments with:
                   - Highest price appreciation potential
                   - Best infrastructure development plans
                   - Best connectivity and amenities
                   - Most favorable regulations for plot development
                
                3. Plot investment recommendations:
                   - Best locations for long-term land banking
                   - Best locations for immediate development
                   - Areas showing emerging potential for plot investments
                   - Risk factors to consider in different areas
                
                4. Specific advice for plot investors based on these trends

                Format the response as follows:
                
                📊 PLOT PRICE TRENDS BY LOCATION
                • [Analysis for each location]

                🏆 TOP PLOT INVESTMENT AREAS
                • [Analysis of best areas for plots]

                💡 PLOT INVESTMENT STRATEGIES
                • [Strategic advice for different plot investment approaches]

                🚧 DEVELOPMENT POTENTIAL ANALYSIS
                • [Analysis of which areas have best development prospects]

                🎯 RECOMMENDATIONS FOR PLOT BUYERS
                • [Specific advice for plot purchase decisions]
                """
            )
            
            return analysis.content
            
        return "No price trends data available for plots in this area"

def create_property_agent():
    """Create PropertyFindingAgent with API keys from environment variables"""
    if 'property_agent' not in st.session_state:
        st.session_state.property_agent = PropertyFindingAgent(
            firecrawl_api_key=os.getenv('FIRECRAWL_API_KEY'),
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            model_id=st.session_state.model_id
        )

def main():
    st.set_page_config(
        page_title="AI Real Estate Agent",
        page_icon="🏠",
        layout="wide"
    )
    
    # Add CSS for flash cards
    st.markdown("""
    <style>
    .property-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s, box-shadow 0.3s;
        cursor: pointer;
    }
    .property-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .property-price {
        font-size: 22px;
        font-weight: bold;
        color: #1e88e5;
    }
    .property-address {
        font-style: italic;
        color: #555;
    }
    .property-features {
        margin-top: 10px;
    }
    .property-cta {
        background-color: #4CAF50;
        color: white;
        padding: 8px 15px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        border-radius: 5px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.title("⚙️ Configuration")
        
        st.subheader("🤖 Model Selection")
        model_id = st.selectbox(
            "Choose OpenAI Model",
            options=["o3-mini", "gpt-4o"],
            help="Select the AI model to use. Choose gpt-4o if your api doesn't have access to o3-mini"
        )
        st.session_state.model_id = model_id

    st.title("🏠 AI Plot Finder")
    st.info(
        """
        Welcome to the AI Plot Finder! 
        Enter your search criteria below to discover available plots 
        and get location insights for your investment.
        """
    )

    col1, col2 = st.columns(2)
    
    with col1:
        city = st.text_input(
            "City",
            placeholder="Enter city name (e.g., Bangalore)",
            help="Enter the city where you want to search for plots"
        )
        
        property_category = st.selectbox(
            "Property Category",
            options=["Residential", "Commercial", "Agricultural"],
            help="Select the type of plot you're interested in"
        )

    with col2:
        max_price = st.number_input(
            "Maximum Price (in Crores)",
            min_value=0.1,
            max_value=100.0,
            value=5.0,
            step=0.1,
            help="Enter your maximum budget in Crores"
        )
        
        property_type = "Plot"  # Fixed to Plot as we're focusing only on plots
        st.info("🔍 Searching for plots only")

    if st.button("🔍 Find Plots", use_container_width=True):
        if not os.getenv('FIRECRAWL_API_KEY') or not os.getenv('OPENAI_API_KEY'):
            st.error("⚠️ API keys not found in environment variables!")
            return
            
        if not city:
            st.error("⚠️ Please enter a city name!")
            return
            
        try:
            create_property_agent()
            with st.spinner("🔍 Searching for plots..."):
                property_results = st.session_state.property_agent.find_properties(
                    city=city,
                    max_price=max_price,
                    property_category=property_category,
                    property_type=property_type
                )
                
                st.success("✅ Plot search completed!")
                
                # Split HTML cards from analysis text
                if "---ANALYSIS_SECTION_BELOW---" in property_results:
                    html_cards, analysis_text = property_results.split("---ANALYSIS_SECTION_BELOW---", 1)
                else:
                    html_cards = ""
                    analysis_text = property_results
                
                st.subheader("🏘️ Recommended Plots")
                # Render HTML cards
                st.markdown(html_cards, unsafe_allow_html=True)
                
                # Display analysis text
                st.markdown(analysis_text)
                
                st.divider()
                
                with st.spinner("📊 Analyzing location trends..."):
                    location_trends = st.session_state.property_agent.get_location_trends(city)
                    
                    st.success("✅ Location analysis completed!")
                    
                    with st.expander("📈 Location Trends Analysis for Plot Investment"):
                        st.markdown(location_trends)
                
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
