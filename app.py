import streamlit as st
from data_providers import NotionData, GoogleSheetsData
from stock_analyzer import StockData, StockPredictor
from data_manager import DataManager
# from github_uploader import GitHubUploader
from config import Config
import os

class StreamlitDashboard:
    """Class for displaying Streamlit dashboard"""
    def __init__(self, stock_data, predictor, data_manager):
        self.stock_data = stock_data
        self.predictor = predictor
        self.data_manager = data_manager

    def run_dashboard(self):
        """Run Streamlit dashboard"""
        st.title("WealthSync Dashboard")
        
        # Create tabs for different views
        tab1, tab2 = st.tabs(["Stock Analysis", "Financial Data"])
        
        with tab1:
            self._show_stock_analysis()
            
        with tab2:
            self._show_financial_data()
    
    def _show_stock_analysis(self):
        """Show stock analysis section"""
        st.header("Stock Analysis")
        ticker = st.selectbox("Choose stock ticker", list(self.stock_data.keys()))
        
        if ticker:
            data = self.stock_data[ticker]
            data['MA50'] = data['Close'].rolling(window=50).mean()
            data = data.dropna()

            features = ['MA50', 'Volume']
            target = 'Close'
            
            if not data.empty and len(data) > 10:  # Ensure enough data for prediction
                predictions = self.predictor.train_model(data, features, target)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Actual Price Chart")
                    st.line_chart(data['Close'])
                
                with col2:
                    st.subheader("Predicted Price Chart")
                    st.line_chart(predictions)
                
                # Show available data files
                st.subheader("Available Data Files")
                data_files = self.data_manager.get_available_data_files()
                if ticker in data_files['stocks']:
                    st.write(f"CSV files for {ticker}:")
                    for file in data_files['stocks'][ticker]:
                        st.write(f"- {file}")
            else:
                st.error(f"Not enough data for {ticker} to make predictions")
    
    def _show_financial_data(self):
        """Show financial data section"""
        st.header("Financial Data")
        
        # Load and display finance data
        finance_data = self.data_manager.load_finance_data()
        if not finance_data.empty:
            # Show summary statistics
            st.subheader("Summary Statistics")
            total_amount = finance_data['Amount'].sum()
            avg_amount = finance_data['Amount'].mean()
            transaction_count = len(finance_data)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Amount", f"${total_amount:,.2f}")
            col2.metric("Average Transaction", f"${avg_amount:,.2f}")
            col3.metric("Transaction Count", transaction_count)
            
            # Show transactions by category
            st.subheader("Transactions by Category")
            category_data = finance_data.groupby('Category')['Amount'].sum()
            st.bar_chart(category_data)
            
            # Show raw data
            st.subheader("Raw Data")
            st.dataframe(finance_data)
            
            # Show available finance files
            st.subheader("Available Finance Files")
            data_files = self.data_manager.get_available_data_files()
            if data_files['finance']:
                st.write("CSV files:")
                for file in data_files['finance']:
                    st.write(f"- {file}")
        else:
            st.warning("No financial data available")

class WealthSync:
    """Main class to orchestrate the entire project"""
    def __init__(self):
        self.config = Config()
        
    def run(self):
        """Run the entire workflow"""
        # Step 1: Fetch data from Notion
        notion = NotionData(self.config.notion_token, self.config.notion_database_id)
        notion_data = notion.fetch_data()

        # Step 2: Fetch data from Google Sheets
        google_sheets = GoogleSheetsData(self.config.credentials_file, self.config.scope)
        tickers = google_sheets.fetch_stock_list(self.config.stock_spreadsheet_id)
        finance_data = google_sheets.fetch_finance_data(self.config.finance_spreadsheet_id)

        # Step 3: Fetch stock data
        stocks = StockData()
        stock_data = stocks.fetch_stock_data(tickers)

        # Step 4: Save data to CSV files
        data_manager = DataManager(self.config.folder_path)
        combined_finance = data_manager.combine_finance_data(notion_data, finance_data)
        data_manager.save_stock_data(stock_data)

        # Step 5: Train Machine Learning model
        predictor = StockPredictor()
        for ticker in tickers:
            if ticker in stock_data:
                data = stock_data[ticker]
                data['MA50'] = data['Close'].rolling(window=50).mean()
                data = data.dropna()
                if not data.empty and len(data) > 10:
                    print(f"Training model for {ticker}")
                    predictor.train_model(data, ['MA50', 'Volume'], 'Close')

        # Step 6: Run Streamlit dashboard
        dashboard = StreamlitDashboard(stock_data, predictor, data_manager)
        dashboard.run_dashboard()

        # Step 7: Push to GitHub
        # github = GitHubUploader(
        #     self.config.github_username,
        #     self.config.github_email,
        #     self.config.github_repo_url,
        #     self.config.github_pat
        # )
        
        # Get all CSV files to push
        data_files = data_manager.get_available_data_files()
        files_to_push = []
        
        # Add finance files
        for file in data_files['finance']:
            files_to_push.append(os.path.join(self.config.folder_path, 'finance', file))
        
        # Add stock files
        for ticker, ticker_files in data_files['stocks'].items():
            for file in ticker_files:
                files_to_push.append(os.path.join(self.config.folder_path, 'stocks', ticker, file))
        
        # github.push_to_github(files_to_push) 