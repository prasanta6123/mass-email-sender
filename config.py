"""
config.py

Configuration file for the Mass Email Sender application.
All project paths are managed from this file.
"""

from pathlib import Path
import os

# =====================================================
# Project Root
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

# =====================================================
# Folders
# =====================================================

DATA_DIR = BASE_DIR / "data"
TEMPLATE_DIR = BASE_DIR / "templates"
ATTACHMENT_DIR = BASE_DIR / "attachments"
LOG_DIR = BASE_DIR / "logs"

# =====================================================
# Input Files
# =====================================================

CONTACTS_FILE = DATA_DIR / "CONTACTS_MAIL.csv"
SENDER_FILE = DATA_DIR / "SENDER_MAIL.csv"
IMAP_FILE = DATA_DIR / "IMAP_CREDENTIALS.csv"

# =====================================================
# HTML Template
# =====================================================

EMAIL_TEMPLATE = TEMPLATE_DIR / "email_template.html"

# =====================================================
# Output Files
# =====================================================

SUCCESS_LOG = LOG_DIR / "MAIL_SUCCESS_RECORD.csv"
FAILURE_LOG = LOG_DIR / "MAIL_FAILURE_RECORD.csv"
TOTAL_MAIL_LOG = LOG_DIR / "TOTAL_MAILS_SENT.csv"

# =====================================================
# SMTP Configuration
# =====================================================

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

# =====================================================
# Application Settings
# =====================================================

MAX_EMAILS_PER_SESSION = 500
DELAY_BETWEEN_EMAILS = 3  # seconds

# =====================================================
# Automatically Create Required Folders
# =====================================================

for folder in [
    DATA_DIR,
    TEMPLATE_DIR,
    ATTACHMENT_DIR,
    LOG_DIR
]:
    folder.mkdir(parents=True, exist_ok=True)

# =====================================================
# Utility Function
# =====================================================

def get_latest_attachment():
    """
    Returns the newest PDF file from the attachments folder.
    Returns None if no PDF exists.
    """
    pdf_files = list(ATTACHMENT_DIR.glob("*.pdf"))

    if not pdf_files:
        return None

    return max(pdf_files, key=lambda f: f.stat().st_mtime)
