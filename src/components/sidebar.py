import streamlit as st
from configs.config import Config

def render_sidebar():
    """Render the sidebar with configuration options"""
    st.sidebar.title("WealthSync")
    
    # Handle redirection if set in session state
    if 'redirect_to' in st.session_state:
        selected_page = st.session_state['redirect_to']
        # Clear the redirect after using it
        del st.session_state['redirect_to']
        return selected_page
    
    # Display configuration status
    st.sidebar.header("Configuration")
    
    # Initialize configuration
    config = Config()
    
    # Display data sources status
    st.sidebar.subheader("Data Sources")
    notion_connected = bool(config.notion_token and config.notion_database_id)
    sheets_connected = bool(config.stock_spreadsheet_id and config.finance_spreadsheet_id)
    github_connected = bool(config.github_username and config.github_pat)
    
    st.sidebar.write(f"Notion API: {'✅ Connected' if notion_connected else '❌ Not configured'}")
    st.sidebar.write(f"Google Sheets: {'✅ Connected' if sheets_connected else '❌ Not configured'}")
    st.sidebar.write(f"GitHub: {'✅ Connected' if github_connected else '❌ Not configured'}")
    
    # Navigation
    st.sidebar.header("Navigation")
    
    # Add navigation options
    pages = {
        "Dashboard": "main",
        "Stock Analysis": "stock_analysis", 
        "Financial Data": "financial_data",
        "Settings": "settings"
    }
    
    selected_page = st.sidebar.radio("Go to", list(pages.keys()))
    
    # Return the selected page
    return pages[selected_page] 