import streamlit as st
import requests
import time
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Medicine Explainer",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
        padding: 10px 20px;
    }
    .medicine-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    .medicine-title {
        font-size: 20px;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 10px;
    }
    .medicine-category {
        background-color: #e7f3ff;
        padding: 5px 10px;
        border-radius: 5px;
        display: inline-block;
        font-size: 12px;
        margin-bottom: 10px;
    }
    .price-badge {
        background-color: #90EE90;
        padding: 5px 10px;
        border-radius: 5px;
        display: inline-block;
        font-weight: bold;
        margin: 5px 5px 5px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        border-left: 4px solid #ffc107;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        border-left: 4px solid #dc3545;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        border-left: 4px solid #28a745;
    }
    </style>
    """, unsafe_allow_html=True)

# API Configuration
API_URL = "http://127.0.0.1:8000"

# Session state
if 'selected_medicine' not in st.session_state:
    st.session_state.selected_medicine = None
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'categories' not in st.session_state:
    st.session_state.categories = None


def check_api_health():
    """Check if FastAPI backend is running"""
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return True, data.get('medicines_in_db', 0)
        return False, 0
    except:
        return False, 0


def search_medicines(query):
    """Search medicines via API"""
    try:
        response = requests.get(
            f"{API_URL}/search",
            params={"query": query},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None


def get_medicine_details(medicine_name):
    """Get detailed information for a medicine"""
    try:
        response = requests.get(
            f"{API_URL}/medicine/{medicine_name}",
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Medicine not found: {medicine_name}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None


def get_all_categories():
    """Get all medicine categories"""
    try:
        response = requests.get(f"{API_URL}/categories", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def get_medicines_by_category(category_name):
    """Get all medicines in a category"""
    try:
        response = requests.get(
            f"{API_URL}/category/{category_name}",
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def display_medicine_card(medicine):
    """Display a medicine card"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"<div class='medicine-title'>{medicine['product_name']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='medicine-category'>{medicine['sub_category']}</div>", unsafe_allow_html=True)
    
    with col2:
        if medicine['product_price'] and medicine['product_price'] != 'Price not available':
            st.markdown(f"<div class='price-badge'>₹ {medicine['product_price']}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Salt Composition:** {medicine['salt_composition']}")
        st.markdown(f"**Manufacturer:** {medicine['product_manufactured']}")
    
    with col2:
        if st.button(f"View Details", key=f"detail_{medicine['id']}"):
            st.session_state.selected_medicine = medicine['product_name']
            st.rerun()


def display_medicine_details(medicine):
    """Display detailed medicine information"""
    
    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"# {medicine['product_name']}")
    with col2:
        if st.button("← Back to Search"):
            st.session_state.selected_medicine = None
            st.rerun()
    
    # Basic Info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Category")
        st.markdown(f"<div class='medicine-category'>{medicine['sub_category']}</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Price")
        price = medicine['product_price']
        if price and price != 'Price not available':
            st.markdown(f"<div class='price-badge'>₹ {price}</div>", unsafe_allow_html=True)
        else:
            st.info("Price information not available")
    
    with col3:
        st.markdown("### Manufacturer")
        st.text(medicine['product_manufactured'])
    
    # Salt Composition
    st.markdown("### Salt Composition")
    st.info(medicine['salt_composition'])
    
    # Description
    st.markdown("### What This Medicine Does")
    st.markdown(medicine['medicine_desc'])
    
    # Side Effects
    st.markdown("### Common Side Effects")
    st.markdown(f"<div class='warning-box'>{medicine['side_effects']}</div>", unsafe_allow_html=True)
    
    # Drug Interactions
    st.markdown("### Drug Interactions")
    st.markdown(f"<div class='warning-box'>{medicine['drug_interactions']}</div>", unsafe_allow_html=True)
    
    # Important Note
    st.markdown("### ⚠️ Important Note")
    st.markdown("""
    This information is for educational purposes only and should not replace professional medical advice.
    Always consult your doctor or pharmacist before taking any medicine.
    """)


# Main App
def main():
    # Header
    st.markdown("# 💊 Medicine Explainer AI")
    st.markdown("Understand your medicines in simple language")
    
    # Check API health
    is_healthy, medicine_count = check_api_health()
    
    if not is_healthy:
        st.markdown("""
        <div class='error-box'>
        <strong>⚠️ API Server Not Running</strong><br>
        Please start the FastAPI server first:<br>
        <code>uvicorn main:app --reload</code>
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    st.markdown(f"<div class='success-box'>✅ Connected to database ({medicine_count:,} medicines available)</div>", unsafe_allow_html=True)
    
    # If medicine is selected, show details
    if st.session_state.selected_medicine:
        medicine = get_medicine_details(st.session_state.selected_medicine)
        if medicine:
            display_medicine_details(medicine)
        st.stop()
    
    # Create tabs for different search methods
    tab1, tab2, tab3 = st.tabs(["🔍 Search", "📂 Browse Categories", "🔎 Advanced Search"])
    
    # Tab 1: Simple Search
    with tab1:
        st.markdown("### Search for a Medicine")
        
        search_query = st.text_input(
            "Enter medicine name, category, or ingredient",
            placeholder="e.g., Paracetamol, Aspirin, Insulin",
            key="simple_search"
        )
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            search_button = st.button("🔍 Search", key="search_btn")
        
        with col2:
            st.write("")  # Spacing
        
        with col3:
            st.write("")  # Spacing
        
        if search_button:
            if not search_query.strip():
                st.warning("Please enter a search query")
            else:
                with st.spinner("🔄 Searching..."):
                    results = search_medicines(search_query)
                
                if results and results['total_results'] > 0:
                    st.markdown(f"### Found {results['total_results']} medicine(s)")
                    
                    for medicine in results['medicines']:
                        with st.container():
                            display_medicine_card(medicine)
                
                elif results:
                    st.info(f"No medicines found for '{search_query}'")
                else:
                    st.error("Error searching medicines. Please try again.")
    
    # Tab 2: Browse Categories
    with tab2:
        st.markdown("### Browse by Category")
        
        with st.spinner("Loading categories..."):
            categories_data = get_all_categories()
        
        if categories_data and categories_data['categories']:
            # Create columns for category buttons
            cols = st.columns(3)
            
            for idx, category_item in enumerate(categories_data['categories']):
                with cols[idx % 3]:
                    category_name = category_item['name']
                    count = category_item['count']
                    
                    if st.button(f"{category_name}\n({count} medicines)", key=f"cat_{category_name}"):
                        with st.spinner(f"Loading {category_name}..."):
                            category_medicines = get_medicines_by_category(category_name)
                        
                        if category_medicines and category_medicines['total_results'] > 0:
                            st.markdown(f"### {category_name}")
                            st.markdown(f"**Found {category_medicines['total_results']} medicines**")
                            
                            for medicine in category_medicines['medicines']:
                                with st.container():
                                    display_medicine_card(medicine)
                        else:
                            st.warning(f"No medicines found in {category_name}")
        else:
            st.error("Could not load categories")
    
    # Tab 3: Advanced Search
    with tab3:
        st.markdown("### Advanced Search")
        
        col1, col2 = st.columns(2)
        
        with col1:
            adv_name = st.text_input(
                "Medicine Name",
                placeholder="Partial name search",
                key="adv_name"
            )
            adv_manufacturer = st.text_input(
                "Manufacturer",
                placeholder="e.g., Pfizer",
                key="adv_manufacturer"
            )
        
        with col2:
            # Get categories for dropdown
            categories_data = get_all_categories()
            category_options = ["All Categories"]
            
            if categories_data and categories_data['categories']:
                category_options.extend([cat['name'] for cat in categories_data['categories']])
            
            adv_category = st.selectbox(
                "Category",
                category_options,
                key="adv_category"
            )
        
        if st.button("🔎 Advanced Search"):
            if not adv_name and not adv_manufacturer and adv_category == "All Categories":
                st.warning("Please enter at least one search criteria")
            else:
                with st.spinner("Searching..."):
                    try:
                        params = {"limit": 100}
                        
                        if adv_name:
                            params["name"] = adv_name
                        if adv_manufacturer:
                            params["manufacturer"] = adv_manufacturer
                        if adv_category != "All Categories":
                            params["category"] = adv_category
                        
                        response = requests.get(
                            f"{API_URL}/search/advanced",
                            params=params,
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            results = response.json()
                            
                            if results['total_results'] > 0:
                                st.markdown(f"### Found {results['total_results']} medicine(s)")
                                
                                for medicine in results['medicines']:
                                    with st.container():
                                        display_medicine_card(medicine)
                            else:
                                st.info("No medicines found matching your criteria")
                        else:
                            st.error("Error during search")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")


if __name__ == '__main__':
    main()
