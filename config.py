import os
from pathlib import Path
from dotenv import load_dotenv

# Initialize environment variables
load_dotenv()

# --- Path Configuration ---
# Resolves the absolute path to the directory containing this file
BASE_DIR = Path(__file__).resolve().parent

# Define core directories
DATA_DIR = BASE_DIR / "data"
TEMPLATE_DIR = BASE_DIR / "templates"
ATTACHMENT_DIR = BASE_DIR / "attachments"
LOG_DIR = BASE_DIR / "logs"

# Automatically generate required directories if missing
for directory in [DATA_DIR, TEMPLATE_DIR, ATTACHMENT_DIR, LOG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Define exact file paths
CONTACTS_FILE = DATA_DIR / "CONTACTS_MAIL.csv"
SENDER_FILE = DATA_DIR / "SENDER_MAIL.csv"
TEMPLATE_FILE = TEMPLATE_DIR / "email_template.html"
SUCCESS_LOG = LOG_DIR / "MAIL_SUCCESS_RECORD.csv"
FAILURE_LOG = LOG_DIR / "MAIL_FAILURE_RECORD.csv"
TOTAL_LOG = LOG_DIR / "TOTAL_MAILS_SENT.csv"

# --- SMTP & Campaign Settings ---
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
DEFAULT_SUBJECT = os.getenv("DEFAULT_SUBJECT", "Tax Invoice")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 1))

# --- Email Body/Template Defaults ---
DEFAULT_AMOUNT = float(os.getenv("DEFAULT_AMOUNT", 699.00))
DEFAULT_QUANTITY = int(os.getenv("DEFAULT_QUANTITY", 1))
CONTACT_NUMBER = os.getenv("CONTACT_NUMBER", "+1 (888) 722-6369")
