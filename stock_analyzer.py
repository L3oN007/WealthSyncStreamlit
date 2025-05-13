import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

class StockData:
    """Class to manage stock data from yfinance"""
    def __init__(self):
        self.stock_data = {}

    def fetch_stock_data(self, tickers):
        """Fetch stock data from yfinance"""
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                history = stock.history(period="1y")
                if not history.empty:
                    self.stock_data[ticker] = history
                    print(f"Successfully fetched data for {ticker} ({len(history)} records)")
                else:
                    print(f"No data available for {ticker}")
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")
        
        return self.stock_data

class StockPredictor:
    """Class to predict stock prices using Machine Learning"""
    def __init__(self):
        self.model = LinearRegression()
        self.models = {}  # Store models for different tickers

    def train_model(self, data, features, target):
        """Train model with data"""
        if data.empty or len(data) < 10:
            print("Not enough data for training")
            return []
            
        try:
            X = data[features]
            y = data[target]
            
            # Split data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
            
            # Train the model
            self.model.fit(X_train, y_train)
            
            # Make predictions
            predictions = self.model.predict(X_test)
            
            # Calculate error metrics
            mse = mean_squared_error(y_test, predictions)
            rmse = np.sqrt(mse)
            print(f"Model performance - MSE: {mse:.4f}, RMSE: {rmse:.4f}")
            
            return predictions
        except Exception as e:
            print(f"Error training model: {e}")
            return []

    def predict(self, data, features):
        """Predict prices with new data"""
        if data.empty:
            return []
            
        try:
            X = data[features]
            return self.model.predict(X)
        except Exception as e:
            print(f"Error making prediction: {e}")
            return [] 