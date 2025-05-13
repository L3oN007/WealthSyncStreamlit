import streamlit as st
from app import WealthSync
from config import Config
import traceback
import sqlite3
import os

def initialize_session_state():
    """Initialize session state variables"""
    if 'is_running' not in st.session_state:
        st.session_state.is_running = False
    if 'error_message' not in st.session_state:
        st.session_state.error_message = None
    if 'success_message' not in st.session_state:
        st.session_state.success_message = None

def handle_wealthsync_run():
    """Handle WealthSync run with proper error handling"""
    try:
        st.session_state.is_running = True
        st.session_state.error_message = None
        st.session_state.success_message = None
        
        wealthsync = WealthSync()
        wealthsync.run()
        
        st.session_state.success_message = "WealthSync completed successfully!"
    except Exception as e:
        st.session_state.error_message = f"Error: {str(e)}\n{traceback.format_exc()}"
    finally:
        st.session_state.is_running = False

def check_database_lock(db_path):
    """Check if database is locked and attempt to fix"""
    if os.path.exists(db_path):
        try:
            # Try to open and close the database
            conn = sqlite3.connect(db_path, timeout=20)  # Increase timeout
            conn.close()
            return None
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                try:
                    # Force close any existing connections
                    os.system(f"fuser -k {db_path} 2>/dev/null")
                    return "Database was locked. Attempted to release lock."
                except Exception:
                    return "Database is locked. Please close other applications using it."
            return str(e)
    return None

def main():
    """Main entry point for the WealthSync application"""
    # Initialize session state
    initialize_session_state()
    
    # Set page configuration
    st.set_page_config(
        page_title="WealthSync Dashboard",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Display application header
    st.title("WealthSync Financial Dashboard")
    st.subheader("Track, analyze, and predict your financial future")
    
    # Initialize configuration
    config = Config()
    config.ensure_data_directory()
    
    # Check database lock
    db_status = check_database_lock(config.db_path)
    if db_status:
        st.warning(db_status)
    
    # Create sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Display configuration status
        st.subheader("Data Sources")
        notion_connected = bool(config.notion_token and config.notion_database_id)
        sheets_connected = bool(config.stock_spreadsheet_id and config.finance_spreadsheet_id)
        github_connected = bool(config.github_username and config.github_pat)
        
        st.write(f"Notion API: {'✅ Connected' if notion_connected else '❌ Not configured'}")
        st.write(f"Google Sheets: {'✅ Connected' if sheets_connected else '❌ Not configured'}")
        st.write(f"GitHub: {'✅ Connected' if github_connected else '❌ Not configured'}")
        
        # Add a button to run the application
        if st.button("Run WealthSync", disabled=st.session_state.is_running):
            handle_wealthsync_run()
    
    # Display status messages
    if st.session_state.is_running:
        with st.spinner("Running WealthSync..."):
            st.info("Processing data and updating dashboard...")
    
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
        if "database is locked" in st.session_state.error_message:
            st.warning("Try closing other applications that might be using the database.")
    
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
    
    # Display main content
    st.write("""
    ## Welcome to WealthSync
    
    This application helps you track your finances, analyze stock performance, and predict future trends.
    
    ### Features:
    - Import financial data from Notion and Google Sheets
    - Analyze stock performance using historical data
    - Predict future stock prices using machine learning
    - Save data to SQLite database
    - Push code and data to GitHub
    
    To get started, configure your data sources in the sidebar and click "Run WealthSync".
    """)

if __name__ == "__main__":
    main() 