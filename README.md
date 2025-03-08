# 🏠 AI Plot Finder

AI Plot Finder is an intelligent real estate tool that helps users discover and analyze available plots based on their preferences. The application uses AI to search property listings, analyze location trends, and visualize property locations on interactive maps.

## 🌟 Features

- **Property Search:** Find plots based on city, budget, and property category
- **AI-Powered Analysis:** Get intelligent insights about properties and locations
- **Interactive Maps:** Visualize property locations with detailed popups
- **Location Trends:** Analyze price trends and investment potential by area
- **Geographic Insights:** Get detailed analysis of property distribution and area development

## 🔧 Technologies Used

- **Python 3.8+**
- **Streamlit:** For the web application interface
- **Agno:** AI agent framework for intelligent analysis
- **Firecrawl:** Web extraction API for property listings
- **OpenAI API:** Powers the intelligent agents
- **Folium:** Interactive mapping visualization
- **Pydantic:** Data validation and schema definition
- **Python-dotenv:** Environment variable management

## 📁 Project Structure

```
plottrends/
├── agents/
│   ├── mapping_agent.py     # Handles geocoding and map data preparation
│   └── property_agent.py    # Handles property search and analysis
├── models/
│   └── schemas.py           # Pydantic data models and schemas
├── ui/
│   └── styles.py            # CSS styles for the UI components
├── utils/
│   └── map_utils.py         # Utilities for map creation and manipulation
├── app.py                   # Main Streamlit application
├── requirements.txt         # Project dependencies
└── .env                     # Environment variables (not in repo)
```

## 🚀 Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/plottrends.git
   cd plottrends
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

Create a `.env` file in the project root with the following variables:

```
OPENAI_API_KEY=your_openai_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
```

## 🖥️ Usage

1. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

2. Access the application in your web browser (typically at http://localhost:8501).

3. Enter your search criteria:
   - City name (e.g., "Bangalore")
   - Property category (Residential, Commercial, or Agricultural)
   - Maximum budget in Crores

4. Click "Find Plots" to start the search.

5. Explore the results:
   - View property cards with details
   - Interact with the map visualization
   - Read AI-generated analysis and insights
   - Check location trends and investment recommendations

## 📸 Screenshots

(Add screenshots of your application here)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
