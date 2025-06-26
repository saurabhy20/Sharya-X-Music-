# In utils/logger.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('shaurya.log'),
        logging.StreamHandler()
    ]
)

def log_error(error):
    logging.error(f"🚨 ERROR: {error}")
