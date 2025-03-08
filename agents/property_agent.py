from agno.agent import Agent
from agno.models.openai import OpenAIChat
from firecrawl import FirecrawlApp
from models.schemas import PropertiesResponse, LocationsResponse

class PropertyFindingAgent:
    """Agent responsible for finding properties and providing recommendations"""
    
    def __init__(self, firecrawl_api_key: str, openai_api_key: str, model_id: str = "o3-mini"):
        self.agent = Agent(
            model=OpenAIChat(id=model_id, api_key=openai_api_key),
            markdown=True,
            description="I am a real estate expert who helps find and analyze properties based on user preferences."
        )
        self.firecrawl = FirecrawlApp(api_key=firecrawl_api_key)
        self.last_response = None  # Store the last response

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
        
        # Store the raw response
        self.last_response = raw_response
        
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
            
            First, create a wrapper div with class="card-container" and inside it, create 5 HTML divs (one for each plot) with class="property-card" using this structure:
            
            <div class="card-container">
              <div class="property-card">
                <h3>PLOT_NAME</h3>
                <div class="property-price">₹PRICE</div>
                <div class="property-address">LOCATION</div>
                <div class="property-features">
                  <p><strong>Area:</strong> AREA_SQFT sq.ft</p>
                  <p><strong>Dimensions:</strong> DIMENSIONS</p>
                </div>
                <div class="property-description">BRIEF_DESCRIPTION (up to 100 words)</div>
                <a href="PROPERTY_URL" class="property-cta" target="_blank">View Details</a>
              </div>
              <!-- Repeat for all 5 properties -->
            </div>
            
            DO NOT wrap this HTML in triple backticks or markdown code blocks.
            Make sure you replace PROPERTY_URL with the actual URL from the property data.
            The "View Details" button must be an actual <a> link tag, not just a div.
            
            Then, AFTER the card container div, start a new section with "---ANALYSIS_SECTION_BELOW---" followed by your analysis text.

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

            Remember: First provide the HTML card container with all cards inside (without code blocks), then the text analysis AFTER the marker.
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
