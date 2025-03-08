PROPERTY_CARD_CSS = """
<style>
/* Card container styles */
.card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
}

/* Property card basic styles */
.property-card {
    border-radius: 12px;
    padding: 16px;
    width: 280px;
    min-height: 400px;
    box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
    display: flex;
    flex-direction: column;
    margin-bottom: 15px;
    overflow: hidden;
    position: relative;
}

/* Card hover effect */
.property-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 20px rgba(0,0,0,0.2);
}

/* Card color variations - pastel colors */
.property-card:nth-child(5n+1) {
    background-color: #E0F7FA; /* Light blue */
    color: #006064;
}

.property-card:nth-child(5n+2) {
    background-color: #F1F8E9; /* Light green */
    color: #33691E;
}

.property-card:nth-child(5n+3) {
    background-color: #FFF3E0; /* Light orange */
    color: #E65100;
}

.property-card:nth-child(5n+4) {
    background-color: #FCE4EC; /* Light pink */
    color: #880E4F;
}

.property-card:nth-child(5n+5) {
    background-color: #E8EAF6; /* Light indigo */
    color: #1A237E;
}

/* Property name */
.property-card h3 {
    margin-top: 0;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 8px;
    line-height: 1.3;
    height: 46px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}

/* Property price */
.property-price {
    font-size: 22px;
    font-weight: bold;
    margin: 10px 0;
}

/* Property address */
.property-address {
    font-style: italic;
    margin-bottom: 10px;
    font-size: 14px;
    height: 40px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}

/* Property features */
.property-features {
    margin-top: 10px;
    font-size: 14px;
}

/* Property description */
.property-description {
    font-size: 13px;
    margin: 10px 0;
    height: 100px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 5;
    -webkit-box-orient: vertical;
    flex-grow: 1;
}

/* CTA button */
.property-cta {
    padding: 8px 15px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    border-radius: 5px;
    margin-top: 10px;
    font-weight: bold;
    align-self: center;
    width: 80%;
    cursor: pointer;
}

/* CTA button color variations to match card colors */
.property-card:nth-child(5n+1) .property-cta {
    background-color: #006064;
    color: white !important;
}

.property-card:nth-child(5n+2) .property-cta {
    background-color: #33691E;
    color: white !important;
}

.property-card:nth-child(5n+3) .property-cta {
    background-color: #E65100;
    color: white !important;
}

.property-card:nth-child(5n+4) .property-cta {
    background-color: #880E4F;
    color: white !important;
}

.property-card:nth-child(5n+5) .property-cta {
    background-color: #1A237E;
    color: white !important;
}

/* Fix Streamlit's link styling */
.property-cta:hover {
    text-decoration: none !important;
    color: white !important;
}
</style>
"""

def apply_styles(st):
    """Apply custom styles to the Streamlit app"""
    st.markdown(PROPERTY_CARD_CSS, unsafe_allow_html=True)
