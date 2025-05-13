import streamlit as st
import os
from configs.config import Config
import yaml
import datetime

def read_log_file(log_path, num_lines=100):
    """Read the last n lines from a log file"""
    if not os.path.exists(log_path):
        return f"Log file not found: {log_path}"
    
    try:
        with open(log_path, 'r') as file:
            lines = file.readlines()
        
        # Get the last n lines
        last_lines = lines[-num_lines:] if len(lines) > num_lines else lines
        return ''.join(last_lines)
    except Exception as e:
        return f"Error reading log file: {str(e)}"

def render_settings():
    """Render the settings page"""
    st.title("Settings")
    
    # Load the current configuration
    config = Config()
    
    # Create tabs for different settings
    tab1, tab2, tab3 = st.tabs(["API Configuration", "Data Storage", "Logs Viewer"])
    
    # Tab 1: API Configuration
    with tab1:
        st.write("Configure your WealthSync application settings here.")
        
        # Notion API Settings
        st.subheader("Notion API")
        notion_token = st.text_input("Notion API Token", config.notion_token, type="password")
        notion_database_id = st.text_input("Notion Database ID", config.notion_database_id)
        
        # Google Sheets Settings
        st.subheader("Google Sheets")
        stock_spreadsheet_id = st.text_input("Stock Spreadsheet ID", config.stock_spreadsheet_id)
        finance_spreadsheet_id = st.text_input("Finance Spreadsheet ID", config.finance_spreadsheet_id)
        
        # GitHub Settings
        st.subheader("GitHub")
        github_username = st.text_input("GitHub Username", config.github_username)
        github_email = st.text_input("GitHub Email", config.github_email)
        github_repo_url = st.text_input("GitHub Repository URL", config.github_repo_url)
        github_pat = st.text_input("GitHub Personal Access Token", config.github_pat, type="password")
        
        # Save Configuration
        if st.button("Save Configuration"):
            # Update configuration with new values
            config.notion_token = notion_token
            config.notion_database_id = notion_database_id
            config.stock_spreadsheet_id = stock_spreadsheet_id
            config.finance_spreadsheet_id = finance_spreadsheet_id
            config.github_username = github_username
            config.github_email = github_email
            config.github_repo_url = github_repo_url
            config.github_pat = github_pat
            
            # Ensure config directory exists
            os.makedirs("configs", exist_ok=True)
            
            # Save configuration to file
            config_path = os.path.join("configs", "config.yaml")
            config.save_config(config_path)
            
            st.success(f"Configuration saved to {config_path}")
        
        # Environment Variables
        st.subheader("Environment Variables")
        st.write("""
        For security, you can also set these values as environment variables:
        
        - `NOTION_TOKEN`
        - `NOTION_DATABASE_ID`
        - `STOCK_SPREADSHEET_ID`
        - `FINANCE_SPREADSHEET_ID`
        - `GITHUB_USERNAME`
        - `GITHUB_EMAIL`
        - `GITHUB_REPO_URL`
        - `GITHUB_PAT`
        - `GOOGLE_CREDENTIALS` (path to credentials.json file)
        """)
    
    # Tab 2: Data Storage Settings
    with tab2:
        st.subheader("Data Storage Settings")
        
        # Data directories
        data_dir = st.text_input("Data Directory", config.data_dir)
        raw_data_dir = st.text_input("Raw Data Directory", config.raw_data_dir)
        processed_data_dir = st.text_input("Processed Data Directory", config.processed_data_dir)
        output_dir = st.text_input("Output Directory", config.output_dir)
        logs_dir = st.text_input("Logs Directory", config.logs_dir)
        
        if st.button("Save Storage Settings"):
            # Update configuration
            config.data_dir = data_dir
            config.raw_data_dir = raw_data_dir
            config.processed_data_dir = processed_data_dir
            config.output_dir = output_dir
            config.logs_dir = logs_dir
            
            # Save configuration
            config_path = os.path.join("configs", "config.yaml")
            config.save_config(config_path)
            
            # Ensure directories exist
            config.ensure_data_directory()
            
            st.success("Storage settings saved and directories created.")
        
        # Data Management
        st.subheader("Data Management")
        
        # Clear data button
        if st.button("Clear All Data"):
            if st.checkbox("I understand this will delete all data files"):
                # Create confirmation dialog
                confirmation = st.text_input("Type 'CONFIRM' to proceed with data deletion:")
                if confirmation == "CONFIRM":
                    # Logic to delete all data files
                    st.warning("This feature is not yet implemented")
                    st.info("You can manually delete files from the data directory")
                else:
                    st.warning("Confirmation text doesn't match. Data not deleted.")
        
        # Display current data storage info
        st.subheader("Data Storage Information")
        
        # Ensure directories exist
        config.ensure_data_directory()
        
        # Get directory sizes
        data_size = sum(os.path.getsize(os.path.join(config.data_dir, f)) for f in os.listdir(config.data_dir) if os.path.isfile(os.path.join(config.data_dir, f)))
        
        # Display info
        st.write(f"Data directory: {os.path.abspath(config.data_dir)}")
        st.write(f"Total data size: {data_size / 1024:.2f} KB")
    
    # Tab 3: Logs Viewer
    with tab3:
        st.subheader("Logs Viewer")
        
        # Get available log files
        logs_dir = config.logs_dir
        log_files = []
        
        if os.path.exists(logs_dir):
            log_files = [f for f in os.listdir(logs_dir) if f.endswith('.log')]
        
        if not log_files:
            st.info("No log files found.")
        else:
            # Select log file to view
            selected_log = st.selectbox("Select log file to view", log_files)
            
            # Display the number of lines to show
            num_lines = st.slider("Number of lines to display", min_value=10, max_value=500, value=100, step=10)
            
            # Display log content
            log_path = os.path.join(logs_dir, selected_log)
            log_content = read_log_file(log_path, num_lines)
            
            # Add download button for the log file
            with open(log_path, 'r') as file:
                full_log = file.read()
                
            st.download_button(
                label="Download Full Log",
                data=full_log,
                file_name=selected_log,
                mime="text/plain"
            )
            
            # Display clear log button
            if st.button("Clear Log"):
                try:
                    with open(log_path, 'w') as file:
                        file.write(f"Log cleared on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    st.success(f"Log file {selected_log} cleared successfully.")
                    # Refresh the display
                    st.rerun()
                except Exception as e:
                    st.error(f"Error clearing log file: {str(e)}")
            
            # Display log content in a code block
            st.code(log_content, language="log") 