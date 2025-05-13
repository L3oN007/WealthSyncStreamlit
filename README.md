# WealthSync Financial Dashboard

A comprehensive financial data visualization and analysis dashboard built with Streamlit.

## Project Structure

```
WealthSyncStreamlit/
├── configs/            # Configuration files
│   └── config.py       # Configuration management
├── data/               # Data storage
│   ├── raw/            # Raw data from sources
│   └── processed/      # Processed data ready for analysis
├── logs/               # Application logs
├── output/             # Generated outputs and reports
├── pages/              # Streamlit pages
│   ├── dashboard/      # Main dashboard pages
│   ├── analytics/      # Data analysis pages
│   └── settings/       # Application settings pages
├── src/                # Source code
│   ├── components/     # Reusable UI components
│   ├── models/         # Machine learning models
│   ├── services/       # Data services and providers
│   └── utils/          # Utility functions
├── main.py             # Application entry point
├── wealth_sync_app.py    # Streamlit application
├── streamlit_run.sh    # Shell script to run the application
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Features

- Financial data visualization and analysis
- Stock market data analysis with price predictions
- Integration with Notion and Google Sheets
- GitHub data synchronization
- Customizable dashboard with multiple views

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/WealthSyncStreamlit.git
   cd WealthSyncStreamlit
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables in file `.env`:
   - `NOTION_TOKEN`
   - `NOTION_DATABASE_ID`
   - `STOCK_SPREADSHEET_ID`
   - `FINANCE_SPREADSHEET_ID`
   - `GITHUB_USERNAME`
   - `GITHUB_EMAIL`
   - `GITHUB_REPO_URL`
   - `GITHUB_PAT`

5. Run the Streamlit app:
   ```
   # Using streamlit directly
   streamlit run streamlit_app.py
   
   # OR using the provided script
   chmod +x streamlit_run.sh
   ./streamlit_run.sh
   ```

## Usage

1. Configure your data sources in the Settings page
2. View financial overview in the Dashboard page
3. Analyze stock data in the Stock Analysis page
4. Explore financial transactions in the Financial Data page

## Data Sources

- **Notion** - For tracking expenses and financial transactions
- **Google Sheets** - For tracking stocks and investments

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 