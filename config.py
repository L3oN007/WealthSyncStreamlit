import os
from dotenv import load_dotenv
from pathlib import Path

class Config:
    """Configuration class for WealthSync application"""
    def __init__(self):
        # Load environment variables from .env file
        env_path = Path('.env')
        load_dotenv(dotenv_path=env_path)
        
        # Data paths
        self.folder_path = os.getenv('WEALTHSYNC_DATA_PATH', './data')
        self.db_path = f'{self.folder_path}/wealthsync_data.db'
        self.credentials_file = os.getenv('GOOGLE_CREDENTIALS_PATH', './credentials.json')
        
        # Notion configuration
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.notion_database_id = os.getenv('NOTION_DATABASE_ID')
        
        # Google Sheets configuration
        self.scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        self.stock_spreadsheet_id = os.getenv('STOCK_SPREADSHEET_ID')
        self.finance_spreadsheet_id = os.getenv('FINANCE_SPREADSHEET_ID')
        
        # GitHub configuration
        self.github_username = os.getenv('GITHUB_USERNAME')
        self.github_email = os.getenv('GITHUB_EMAIL')
        self.github_pat = os.getenv('GITHUB_PAT')
        self.github_repo_url = f"https://{self.github_pat}@github.com/{self.github_username}/WealthSync.git" if self.github_pat else ''
        
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            print(f"Created folder: {self.folder_path}")
        else:
            print(f"Folder already exists: {self.folder_path}") 