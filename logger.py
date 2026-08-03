import logging
import csv
from datetime import datetime
import config

def setup_logger(name="mass_mailer"):
    """
    Configures and returns a dual-stream logger.
    Outputs INFO to the console and DEBUG/ERROR to a local file.
    """
    logger = logging.getLogger(name)
    
    # Prevent adding multiple handlers if setup_logger is called multiple times
    # across different modules.
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(logging.DEBUG)

    # Console Handler (For real-time monitoring)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_format)

    # File Handler (For debugging and error tracking)
    log_file_path = config.LOG_DIR / "application.log"
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

def log_campaign_metrics(total_sent: int):
    """
    Logs the total number of emails sent during the session to a CSV file.
    Maintains compatibility with the original project's reporting structure.
    """
    logger = logging.getLogger("mass_mailer")
    
    now = datetime.now()
    date_str = now.strftime("%d-%b-%Y")
    time_str = now.strftime("%H:%M")
    
    record = [date_str, time_str, total_sent]
    
    try:
        with open(config.TOTAL_LOG, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(record)
        logger.info(f"Campaign metrics appended to {config.TOTAL_LOG.name}: {total_sent} sent.")
    except PermissionError:
        logger.error(f"Permission denied: Could not write metrics to {config.TOTAL_LOG.name}. Is the file open?")
    except Exception as e:
        logger.error(f"Could not write to metrics log: {e}")
