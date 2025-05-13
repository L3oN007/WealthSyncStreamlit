#!/usr/bin/env python3
"""
Setup environment for WealthSync application.
This script creates a .env file if it doesn't exist.
"""

import os
import sys

def setup_env():
    """Create .env file if it doesn't exist"""
    env_file = '.env'
    env_example = '.env.example'
    
    # Check if .env file exists
    if os.path.exists(env_file):
        print(f"{env_file} already exists. Skipping creation.")
        return
    
    # Create .env file with default content
    default_content = """# WealthSync Environment Variables
# Update with your credentials

# Notion API Credentials
NOTION_TOKEN=
NOTION_DATABASE_ID=

# Google Sheets Configuration
GOOGLE_CREDENTIALS=credentials.json
STOCK_SPREADSHEET_ID=
FINANCE_SPREADSHEET_ID=

# GitHub Configuration
GITHUB_USERNAME=
GITHUB_EMAIL=
GITHUB_REPO_URL=https://github.com/yourusername/your-repo
GITHUB_PAT=
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(default_content)
        print(f"Created {env_file} file. Please update it with your credentials.")
    except Exception as e:
        print(f"Error creating {env_file}: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(setup_env()) 