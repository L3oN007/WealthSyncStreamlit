import streamlit as st
import os
from dotenv import load_dotenv
from src.components.sidebar import render_sidebar
from pages.dashboard.main_dashboard import render_dashboard
from pages.analytics.stock_analysis import render_stock_analysis
from pages.analytics.financial_data import render_financial_data
from pages.settings.settings_page import render_settings
from src.utils.logger import setup_logger

# Load environment variables from .env file
load_dotenv()

# Set up logger
logger = setup_logger("wealth_sync_app")

def main():
    """Main function to run the Streamlit application"""
    # Configure the Streamlit page
    st.set_page_config(
        page_title="WealthSync Dashboard",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    try:
        # Render the sidebar and get the selected page
        selected_page = render_sidebar()
        
        # Render the selected page
        if selected_page == "main":
            render_dashboard()
        elif selected_page == "stock_analysis":
            render_stock_analysis()
        elif selected_page == "financial_data":
            render_financial_data()
        elif selected_page == "settings":
            render_settings()
        else:
            st.error(f"Unknown page: {selected_page}")
            
    except Exception as e:
        logger.error(f"Error in Streamlit app: {e}")
        st.error(f"An error occurred: {str(e)}")
        st.write("Please check the logs for more details.")

if __name__ == "__main__":
    main() 