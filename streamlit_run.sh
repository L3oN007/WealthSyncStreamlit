#!/bin/bash

# Ensure virtual environment is activated
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Check if requirements are installed
if ! pip show streamlit > /dev/null 2>&1; then
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

# Ensure data directories exist
mkdir -p data/raw data/processed output logs

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Setting up environment variables..."
    python setup_env.py
fi

# Run the Streamlit application
echo "Starting WealthSync Dashboard..."
streamlit run main.py 