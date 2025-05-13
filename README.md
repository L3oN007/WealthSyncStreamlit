# WealthSync 📊

[![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

WealthSync is a powerful financial dashboard application that combines data from multiple sources to provide comprehensive financial insights. It leverages machine learning for stock predictions and offers an intuitive Streamlit interface for seamless interaction with your financial data.

## 🌟 Features

### Data Integration
- 📝 Import financial transactions from Notion databases
- 📊 Sync with Google Sheets for stock and financial data
- 💾 Automatic data persistence using SQLite
- 🔄 Automated GitHub backup integration

### Analytics
- 📈 Real-time stock performance analysis
- 🤖 ML-powered stock price predictions
- 📉 Historical trend visualization
- 💰 Financial health indicators

### Dashboard
- 🎯 Interactive data visualization
- 📱 Responsive design
- 🔍 Advanced filtering capabilities
- 📤 Export functionality

## 🚀 Prerequisites

Before you begin, ensure you have:

- Python 3.8 or higher installed
- Git installed
- Access to Notion (with API access)
- Google Cloud project with Sheets API enabled
- GitHub account for backup functionality

## 🛠️ Project Structure

```
WealthSyncStreamlit/
│
├── app.py              # Main application logic
├── config.py           # Configuration management
├── data_manager.py     # Data operations
├── data_providers.py   # External data source integrations
├── github_uploader.py  # GitHub backup functionality
├── stock_analyzer.py   # Stock analysis and ML predictions
├── data/               # Data storage directory
├── .env.example        # Environment variables template
├── .gitignore
├── main.py             # Application entry point
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
```

## ⚙️ Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/WealthSync.git
   cd WealthSync
   ```

2. **Set Up Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv .venv

   # Activate virtual environment
   # Windows (CMD)
   .venv\Scripts\activate.bat
   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   - Copy `.env.example` to `.env`
   ```bash
   cp .env.example .env
   ```
   - Update the following variables in `.env`:
   ```bash
   # Data Storage
   WEALTHSYNC_DATA_PATH="./data"
   GOOGLE_CREDENTIALS_PATH="./credentials.json"

   # Notion Configuration
   NOTION_TOKEN="your_notion_token"
   NOTION_DATABASE_ID="your_notion_database_id"

   # Google Sheets Configuration
   STOCK_SPREADSHEET_ID="your_stock_spreadsheet_id"
   FINANCE_SPREADSHEET_ID="your_finance_spreadsheet_id"

   # GitHub Configuration
   GITHUB_USERNAME="your_github_username"
   GITHUB_EMAIL="your_github_email"
   GITHUB_PAT="your_github_personal_access_token"
   ```

5. **Run the Application**
   ```bash
   streamlit run main.py
   ```

## 📊 Data Source Requirements

### Notion Database Structure
Your Notion database should include:
- `Date` (Date type)
- `Category` (Select type)
- `Description` (Title type)
- `Amount` (Number type)

### Google Sheets Structure
1. **Stock List Spreadsheet**
   - Column A: Ticker symbols
   - Column B: Company names (optional)

2. **Finance Data Spreadsheet**
   - Must match Notion database structure
   - Date format: YYYY-MM-DD

## 🤖 Machine Learning Component

The stock price prediction model uses:

### Features
- 50-day Moving Average
- Trading Volume
- Historical price patterns
- Market indicators

### Model Details
- Algorithm: Linear Regression
- Training period: 2 years of historical data
- Prediction horizon: 30 days
- Accuracy metrics available in the dashboard



## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

For support or queries, please open an issue in the GitHub repository. 