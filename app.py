import streamlit as st
import os
from dotenv import load_dotenv
from streamlit_folium import folium_static
import traceback

# Import from local modules
from models import PropertyLocation
from agents import PropertyFindingAgent, LocationMappingAgent
from utils import create_map_with_properties
from ui import apply_styles

# Load environment variables from .env file
load_dotenv()

def create_agents():
    """Create the agent pipeline from environment variables"""
    if 'property_agent' not in st.session_state:
        st.session_state.property_agent = PropertyFindingAgent(
            firecrawl_api_key=os.getenv('FIRECRAWL_API_KEY'),
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            model_id=st.session_state.model_id
        )
    
    if 'mapping_agent' not in st.session_state:
        st.session_state.mapping_agent = LocationMappingAgent(
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            model_id=st.session_state.model_id
        )

def main():
    st.set_page_config(
        page_title="AI Plot Finder",
        page_icon="🏠",
        layout="wide"
    )
    
    # Apply CSS styles
    apply_styles(st)

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
            create_agents()
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
                
                # Process raw property data for mapping
                raw_response = st.session_state.property_agent.last_response
                if isinstance(raw_response, dict) and raw_response.get('success'):
                    properties = raw_response['data'].get('properties', [])
                    
                    with st.spinner("🗺️ Mapping property locations..."):
                        # Use the mapping agent to get coordinates
                        property_locations = st.session_state.mapping_agent.process_properties(properties, city)
                        
                        st.subheader("🗺️ Property Map")
                        if property_locations:
                            # Create and display map
                            m = create_map_with_properties(property_locations, city)
                            folium_static(m, width=800, height=500)
                            
                            # Geographic insights
                            with st.expander("🧭 Geographic Analysis"):
                                geo_insights = st.session_state.mapping_agent.generate_area_insights(property_locations, city)
                                st.markdown(geo_insights)
                        else:
                            st.warning("⚠️ Could not map property locations")
                
                st.divider()
                
                with st.spinner("📊 Analyzing location trends..."):
                    location_trends = st.session_state.property_agent.get_location_trends(city)
                    
                    st.success("✅ Location analysis completed!")
                    
                    with st.expander("📈 Location Trends Analysis for Plot Investment"):
                        st.markdown(location_trends)
                
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.error(f"Error details: {type(e).__name__}")
            st.code(traceback.format_exc())

if __name__ == "__main__":
    main()

