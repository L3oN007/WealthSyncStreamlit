import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from notion_client import Client
from src.utils.logger import setup_logger

logger = setup_logger("data_providers")

class NotionData:
    """Class to manage data from Notion"""
    def __init__(self, token, database_id):
        self.notion = Client(auth=token)
        self.database_id = database_id
        self.data = None

    def fetch_data(self):
        """Fetch data from Notion"""
        try:
            results = self.notion.databases.query(database_id=self.database_id).get("results")
            data = []
            for page in results:
                date = page["properties"]["Date"]["date"]["start"] if page["properties"]["Date"]["date"] else None
                category = page["properties"]["Category"]["select"]["name"] if page["properties"]["Category"]["select"] else None
                description = page["properties"]["Description"]["title"][0]["text"]["content"] if page["properties"]["Description"]["title"] else None
                amount = page["properties"]["Amount"]["number"] if page["properties"]["Amount"]["number"] else 0
                data.append([date, category, description, amount])
            self.data = pd.DataFrame(data, columns=["Date", "Category", "Description", "Amount"])
            logger.info(f"Successfully fetched {len(data)} records from Notion")
            return self.data
        except Exception as e:
            logger.error(f"Error fetching data from Notion: {e}")
            return pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

class GoogleSheetsData:
    """Class to manage data from Google Sheets"""
    def __init__(self, credentials_path, scope):
        try:
            self.creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
            self.client = gspread.authorize(self.creds)
            logger.info("Successfully connected to Google Sheets")
        except Exception as e:
            logger.error(f"Error connecting to Google Sheets: {e}")
            self.client = None

    def fetch_stock_list(self, spreadsheet_id):
        """Fetch stock list from Google Sheets"""
        if not self.client:
            logger.error("Google Sheets client not initialized")
            return []
            
        try:
            sheet = self.client.open_by_key(spreadsheet_id).sheet1
            tickers = sheet.col_values(1)[1:]  # Skip header row
            logger.info(f"Successfully fetched {len(tickers)} stock tickers")
            return tickers
        except Exception as e:
            logger.error(f"Error fetching stock list: {e}")
            return []

    def fetch_finance_data(self, spreadsheet_id):
        """Fetch financial data from Google Sheets"""
        if not self.client:
            logger.error("Google Sheets client not initialized")
            return pd.DataFrame()
            
        try:
            sheet = self.client.open_by_key(spreadsheet_id).sheet1
            data = pd.DataFrame(sheet.get_all_records())
            logger.info(f"Successfully fetched {len(data)} financial records")
            return data
        except Exception as e:
            logger.error(f"Error fetching finance data: {e}")
            return pd.DataFrame() 