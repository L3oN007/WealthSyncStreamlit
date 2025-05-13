import logging
import os
from datetime import datetime

def setup_logger(name, log_file=None, level=logging.INFO):
    """Set up logger for the application"""
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Check if logger already exists to avoid duplicate handlers
    logger = logging.getLogger(name)
    
    # Return existing logger if it's already set up
    if logger.handlers:
        return logger
    
    # Set the level
    logger.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create console handler and set level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Add console handler to logger
    logger.addHandler(console_handler)
    
    # Create file handler and set level to debug
    if log_file is None:
        # Use a consistent filename for each logger type without date stamp
        log_file = os.path.join(logs_dir, f"{name}.log")
    
    file_handler = logging.FileHandler(log_file, mode='a')  # 'a' for append
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Add file handler to logger
    logger.addHandler(file_handler)
    
    # Log a separator when the logger starts
    logger.info("=" * 80)
    logger.info(f"Logger started on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return logger 