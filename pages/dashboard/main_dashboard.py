import streamlit as st
import pandas as pd
import os
import datetime
from src.services.data_manager import DataManager
from configs.config import Config

def get_last_updated_time(file_path):
    """Get the last modified time of a file"""
    if os.path.exists(file_path):
        mod_time = os.path.getmtime(file_path)
        return datetime.datetime.fromtimestamp(mod_time)
    return None

def load_dashboard_data():
    """Load data for the dashboard"""
    config = Config()
    data_manager = DataManager(config.raw_data_dir)
    
    # Load finance data
    finance_data = data_manager.load_finance_data()
    
    # Get available stock tickers
    data_files = data_manager.get_available_data_files()
    available_tickers = list(data_files['stocks'].keys())
    
    # Load stock data for the first available ticker
    if available_tickers:
        stock_data = data_manager.load_stock_data(available_tickers[0])
        selected_ticker = available_tickers[0]
    else:
        stock_data = pd.DataFrame()
        selected_ticker = None
        
    # Get last updated times
    finance_latest_file = os.path.join(config.raw_data_dir, 'finance', 'finance_data_latest.csv')
    finance_last_updated = get_last_updated_time(finance_latest_file)
    
    stock_last_updated = None
    if selected_ticker:
        stock_latest_file = os.path.join(config.raw_data_dir, 'stocks', selected_ticker, f'{selected_ticker}_latest.csv')
        stock_last_updated = get_last_updated_time(stock_latest_file)
        
    return finance_data, stock_data, available_tickers, selected_ticker, finance_last_updated, stock_last_updated

def render_dashboard():
    """Render the main dashboard"""
    st.title("WealthSync Dashboard")
    
    # Load data
    finance_data, stock_data, available_tickers, selected_ticker, finance_last_updated, stock_last_updated = load_dashboard_data()
    
    # Last updated info
    st.sidebar.subheader("Data Last Updated")
    
    if finance_last_updated:
        st.sidebar.write(f"Finance Data: {finance_last_updated.strftime('%Y-%m-%d %H:%M')}")
    else:
        st.sidebar.write("Finance Data: Never updated")
        
    if stock_last_updated:
        st.sidebar.write(f"Stock Data ({selected_ticker}): {stock_last_updated.strftime('%Y-%m-%d %H:%M')}")
    else:
        st.sidebar.write("Stock Data: Never updated")
    


    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Financial Overview")
        if not finance_data.empty:
            # Calculate key metrics
            total_amount = finance_data['Amount'].sum()
            avg_amount = finance_data['Amount'].mean()
            transaction_count = len(finance_data)
            
            # Display metrics
            st.metric("Total Amount", f"${total_amount:,.2f}")
            st.metric("Average Transaction", f"${avg_amount:,.2f}")
            st.metric("Transaction Count", transaction_count)
        else:
            st.info("No financial data available. Go to Financial Data page to update.")
    
    with col2:
        st.subheader("Stock Performance")
        if not stock_data.empty and 'Close' in stock_data.columns:
            ticker = selected_ticker if selected_ticker else "N/A"
            st.write(f"Showing data for: {ticker}")
            st.line_chart(stock_data['Close'])
        else:
            st.info("No stock data available. Go to Stock Analysis page to update.")
    
    # Show transactions by category
    if not finance_data.empty and 'Category' in finance_data.columns:
        st.subheader("Spending by Category")
        category_data = finance_data.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        st.bar_chart(category_data)
    
    # Recent transactions
    st.subheader("Recent Transactions")
    if not finance_data.empty:
        recent_transactions = finance_data.sort_values('Date', ascending=False).head(5)
        st.dataframe(recent_transactions[['Date', 'Category', 'Description', 'Amount']])
    else:
        st.info("No transaction data available") 