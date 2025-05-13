import pandas as pd
import os
from datetime import datetime

class DataManager:
    """Class to combine and store data in CSV files"""
    def __init__(self, base_path):
        self.base_path = base_path
        self._ensure_data_directory()
        
    def _ensure_data_directory(self):
        """Ensure the directory for data storage exists"""
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
            print(f"Created directory: {self.base_path}")
            
        # Create subdirectories for different data types
        self.finance_dir = os.path.join(self.base_path, 'finance')
        self.stocks_dir = os.path.join(self.base_path, 'stocks')
        
        for directory in [self.finance_dir, self.stocks_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directory: {directory}")

    def _get_timestamp(self):
        """Get current timestamp for file naming"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def combine_finance_data(self, notion_data, google_data):
        """Combine financial data from Notion and Google Sheets"""
        try:
            # Ensure both dataframes have the same columns
            required_columns = ["Date", "Category", "Description", "Amount"]
            for df in [notion_data, google_data]:
                for col in required_columns:
                    if col not in df.columns:
                        df[col] = None
            
            # Combine data
            combined_finance = pd.concat([notion_data, google_data], ignore_index=True)
            
            # Convert date strings to datetime objects
            combined_finance["Date"] = pd.to_datetime(combined_finance["Date"], errors='coerce')
            
            # Sort by date
            combined_finance = combined_finance.sort_values("Date")
            
            # Save to CSV
            timestamp = self._get_timestamp()
            finance_file = os.path.join(self.finance_dir, f'finance_data_{timestamp}.csv')
            combined_finance.to_csv(finance_file, index=False)
            
            # Also save a latest version
            latest_file = os.path.join(self.finance_dir, 'finance_data_latest.csv')
            combined_finance.to_csv(latest_file, index=False)
            
            print(f"Saved {len(combined_finance)} combined finance records to CSV")
            print(f"Files saved: \n- {finance_file}\n- {latest_file}")
            
            return combined_finance
        except Exception as e:
            print(f"Error combining finance data: {e}")
            return pd.DataFrame()

    def save_stock_data(self, stock_data):
        """Save stock data to CSV files"""
        try:
            timestamp = self._get_timestamp()
            saved_files = []
            
            for ticker, df in stock_data.items():
                if not df.empty:
                    # Create ticker directory if it doesn't exist
                    ticker_dir = os.path.join(self.stocks_dir, ticker)
                    if not os.path.exists(ticker_dir):
                        os.makedirs(ticker_dir)
                    
                    # Save timestamped version
                    stock_file = os.path.join(ticker_dir, f'{ticker}_{timestamp}.csv')
                    df.to_csv(stock_file)
                    saved_files.append(stock_file)
                    
                    # Save latest version
                    latest_file = os.path.join(ticker_dir, f'{ticker}_latest.csv')
                    df.to_csv(latest_file)
                    saved_files.append(latest_file)
                    
                    print(f"Saved {len(df)} records for {ticker}")
            
            print(f"Stock data saved to:\n" + "\n".join(f"- {f}" for f in saved_files))
            
        except Exception as e:
            print(f"Error saving stock data: {e}")

    def load_stock_data(self, ticker):
        """Load latest stock data for a ticker"""
        try:
            latest_file = os.path.join(self.stocks_dir, ticker, f'{ticker}_latest.csv')
            if os.path.exists(latest_file):
                df = pd.read_csv(latest_file)
                # Convert index to datetime if it exists
                if 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date'])
                return df
            else:
                print(f"No data found for ticker {ticker}")
                return pd.DataFrame()
        except Exception as e:
            print(f"Error loading stock data for {ticker}: {e}")
            return pd.DataFrame()

    def load_finance_data(self):
        """Load latest finance data"""
        try:
            latest_file = os.path.join(self.finance_dir, 'finance_data_latest.csv')
            if os.path.exists(latest_file):
                df = pd.read_csv(latest_file)
                df['Date'] = pd.to_datetime(df['Date'])
                return df
            else:
                print("No finance data found")
                return pd.DataFrame()
        except Exception as e:
            print(f"Error loading finance data: {e}")
            return pd.DataFrame()

    def get_available_data_files(self):
        """Get list of all available data files"""
        data_files = {
            'finance': [],
            'stocks': {}
        }
        
        # Get finance files
        if os.path.exists(self.finance_dir):
            data_files['finance'] = sorted([
                f for f in os.listdir(self.finance_dir)
                if f.endswith('.csv')
            ])
        
        # Get stock files
        if os.path.exists(self.stocks_dir):
            for ticker in os.listdir(self.stocks_dir):
                ticker_dir = os.path.join(self.stocks_dir, ticker)
                if os.path.isdir(ticker_dir):
                    data_files['stocks'][ticker] = sorted([
                        f for f in os.listdir(ticker_dir)
                        if f.endswith('.csv')
                    ])
        
        return data_files 