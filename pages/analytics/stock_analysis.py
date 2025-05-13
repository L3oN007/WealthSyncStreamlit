import streamlit as st
import pandas as pd
import numpy as np
from src.services.data_manager import DataManager
from src.models.stock_analyzer import StockData, StockPredictor
from src.services.data_providers import GoogleSheetsData
from configs.config import Config
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger("stock_analysis")

def update_stock_data():
    """Fetch and update stock data"""
    with st.spinner("Fetching stock data..."):
        try:
            # Get configuration
            config = Config()
            
            # Initialize Google Sheets data provider
            google_sheets = GoogleSheetsData(config.credentials_file, config.scope)
            
            # Fetch stock tickers
            tickers = google_sheets.fetch_stock_list(config.stock_spreadsheet_id)
            
            if not tickers:
                st.error("No stock tickers found. Please check your Google Sheets configuration.")
                return False
                
            # Fetch stock data
            stock_data_provider = StockData()
            stock_data = stock_data_provider.fetch_stock_data(tickers)
            
            if not stock_data:
                st.error("Failed to fetch any stock data.")
                return False
                
            # Save stock data to files
            data_manager = DataManager(config.raw_data_dir)
            data_manager.save_stock_data(stock_data)
            
            st.success(f"Successfully updated stock data for {len(stock_data)} tickers!")
            return True
            
        except Exception as e:
            logger.error(f"Error updating stock data: {e}")
            st.error(f"Error updating stock data: {str(e)}")
            return False

def render_stock_analysis():
    """Render the stock analysis page"""
    st.title("Stock Analysis")
    
    # Add a button to update data
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🔄 Update Stock Data"):
            success = update_stock_data()
            if success:
                st.experimental_rerun()  # Refresh the page to show updated data
    

    
    # Load configuration and data
    config = Config()
    data_manager = DataManager(config.raw_data_dir)
    
    # Get available stock tickers
    data_files = data_manager.get_available_data_files()
    available_tickers = list(data_files['stocks'].keys())
    
    if not available_tickers:
        st.warning("No stock data available. Please click the 'Update Stock Data' button to fetch stock data.")
        return
    
    # Select ticker
    ticker = st.selectbox("Select Stock", available_tickers)
    
    if ticker:
        # Load stock data
        stock_data = data_manager.load_stock_data(ticker)
        
        if stock_data.empty:
            st.error(f"No data available for {ticker}")
            return
        
        # Display stock data
        st.subheader(f"{ticker} Stock Price")
        st.line_chart(stock_data['Close'])
        
        # Technical indicators
        st.subheader("Technical Indicators")
        
        # Calculate moving averages
        stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['MA200'] = stock_data['Close'].rolling(window=200).mean()
        
        # Drop NaN values
        stock_data = stock_data.dropna()
        
        # Plot moving averages
        st.line_chart({
            'Close': stock_data['Close'],
            'MA50': stock_data['MA50'],
            'MA200': stock_data['MA200']
        })
        
        # Calculate RSI
        delta = stock_data['Close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
        rs = gain / loss
        stock_data['RSI'] = 100 - (100 / (1 + rs))
        
        # Plot RSI
        st.subheader("Relative Strength Index (RSI)")
        st.line_chart(stock_data['RSI'])
        
        # Machine Learning Prediction
        st.subheader("Price Prediction")
        
        if st.button("Run Prediction Model"):
            with st.spinner("Training model and making predictions..."):
                # Features for prediction
                features = ['MA50', 'Volume']
                target = 'Close'
                
                if len(stock_data) > 10:  # Ensure enough data for prediction
                    # Initialize predictor
                    predictor = StockPredictor()
                    
                    # Train model and make predictions
                    predictions = predictor.train_model(stock_data, features, target)
                    
                    if len(predictions) > 0:
                        # Display predictions
                        st.success("Prediction completed!")
                        
                        # Plot actual vs predicted
                        st.subheader("Actual vs Predicted Prices")
                        
                        # Create a dataframe for visualization
                        pred_df = pd.DataFrame({
                            'Actual': stock_data[target].iloc[-len(predictions):].values,
                            'Predicted': predictions
                        })
                        
                        st.line_chart(pred_df)
                        
                        # Calculate prediction accuracy
                        mape = np.mean(np.abs((pred_df['Actual'] - pred_df['Predicted']) / pred_df['Actual'])) * 100
                        st.metric("Mean Absolute Percentage Error", f"{mape:.2f}%")
                    else:
                        st.error("Prediction failed. Please try again.")
                else:
                    st.error(f"Not enough data for {ticker} to make predictions")
        
        # Add a download button for CSV export
        csv = stock_data.to_csv(index=False)
        st.download_button(
            label="Download Stock Data as CSV",
            data=csv,
            file_name=f"{ticker}_stock_data.csv",
            mime="text/csv",
        )
        
        # Display raw data
        st.subheader("Raw Data")
        st.dataframe(stock_data) 