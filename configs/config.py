import os
import yaml
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for WealthSync application"""
    def __init__(self, config_path=None):
        # Default configuration values
        self.data_dir = "data"
        self.raw_data_dir = os.path.join(self.data_dir, "raw")
        self.processed_data_dir = os.path.join(self.data_dir, "processed")
        self.output_dir = "output"
        self.logs_dir = "logs"
        
        # Database configuration
        self.db_path = os.path.join(self.data_dir, "wealthsync.db")
        
        # API Credentials
        self.notion_token = os.environ.get("NOTION_TOKEN", "")
        self.notion_database_id = os.environ.get("NOTION_DATABASE_ID", "")
        
        # Google Sheets configuration
        self.credentials_file = os.environ.get("GOOGLE_CREDENTIALS", "credentials.json")
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.stock_spreadsheet_id = os.environ.get("STOCK_SPREADSHEET_ID", "")
        self.finance_spreadsheet_id = os.environ.get("FINANCE_SPREADSHEET_ID", "")
        
        # GitHub configuration
        self.github_username = os.environ.get("GITHUB_USERNAME", "")
        self.github_email = os.environ.get("GITHUB_EMAIL", "")
        self.github_repo_url = os.environ.get("GITHUB_REPO_URL", "")
        self.github_pat = os.environ.get("GITHUB_PAT", "")
        
        # Data storage folders
        self.folder_path = self.raw_data_dir
        
        # Load configuration from file if provided
        if config_path:
            self.load_config(config_path)
    
    def load_config(self, config_path):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as file:
                config_data = yaml.safe_load(file)
                
            for key, value in config_data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                    
            logging.info(f"Loaded configuration from {config_path}")
        except Exception as e:
            logging.error(f"Error loading configuration: {e}")
    
    def save_config(self, config_path):
        """Save configuration to YAML file"""
        try:
            config_data = {
                'data_dir': self.data_dir,
                'raw_data_dir': self.raw_data_dir,
                'processed_data_dir': self.processed_data_dir,
                'output_dir': self.output_dir,
                'logs_dir': self.logs_dir,
                'db_path': self.db_path,
                'credentials_file': self.credentials_file,
                'scope': self.scope,
                'stock_spreadsheet_id': self.stock_spreadsheet_id,
                'finance_spreadsheet_id': self.finance_spreadsheet_id,
                'github_username': self.github_username,
                'github_email': self.github_email,
                'github_repo_url': self.github_repo_url
            }
            
            with open(config_path, 'w') as file:
                yaml.dump(config_data, file, default_flow_style=False)
                
            logging.info(f"Saved configuration to {config_path}")
        except Exception as e:
            logging.error(f"Error saving configuration: {e}")
    
    def ensure_data_directory(self):
        """Ensure all data directories exist"""
        for directory in [self.data_dir, self.raw_data_dir, self.processed_data_dir, 
                         self.output_dir, self.logs_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logging.info(f"Created directory: {directory}") 