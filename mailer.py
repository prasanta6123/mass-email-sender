import smtplib
import uuid
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
from email.header import Header
from faker import Faker

import config
from logger import setup_logger

logger = setup_logger()
fake = Faker()

class SMTPClient:
    def __init__(self, sender_email: str, sender_password: str):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.server = None
        # Generate a random sender name for the header to avoid spam filters
        self.sender_name = fake.company() 

    def connect(self) -> bool:
        """Establishes a secure TLS connection to the SMTP server."""
        try:
            self.server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
            self.server.starttls()
            self.server.login(self.sender_email, self.sender_password)
            return True
        except smtplib.SMTPAuthenticationError:
            logger.error(f"Authentication failed for {self.sender_email}.")
            return False
        except Exception as e:
            logger.error(f"Connection error for {self.sender_email}: {e}")
            return False

    def disconnect(self):
        """Safely closes the SMTP connection."""
        if self.server:
            try:
                self.server.quit()
            except Exception:
                pass
            finally:
                self.server = None

    def _build_message(self, recipient_email: str, attachment_path=None) -> MIMEMultipart:
        """Constructs the MIME multipart email with dynamic HTML and attachments."""
        message = MIMEMultipart("alternative")
        message['Subject'] = config.DEFAULT_SUBJECT
        message['From'] = formataddr((str(Header(self.sender_name, 'utf-8')), self.sender_email))
        message['To'] = recipient_email

        # Generate dynamic invoice data
        now = datetime.now()
        bill_date = now.strftime("%b %d, %Y")
        due_date = (now + timedelta(days=1)).strftime("%b %d, %Y")
        
        # Generate a random 18-character uppercase invoice number
        invoice_number = str(uuid.uuid1())[5:23].upper()
        
        amount_formatted = "{:.2f}".format(config.DEFAULT_AMOUNT)
        total_amount = "{:.2f}".format(config.DEFAULT_QUANTITY * config.DEFAULT_AMOUNT)

        # Inject data into HTML template
        try:
            with open(config.TEMPLATE_FILE, 'r', encoding="utf8") as f:
                html_content = f.read()
                
            html_content = html_content.replace("INVOICE_VAL", invoice_number)
            html_content = html_content.replace("issued_date", bill_date)
            html_content = html_content.replace("due_date", due_date)
            html_content = html_content.replace("ITEM_QUANTITY", str(config.DEFAULT_QUANTITY))
            html_content = html_content.replace("AMOUNT_VAL1", f"${amount_formatted}")
            html_content = html_content.replace("AMOUNT_VAL", f"${total_amount}")
            html_content = html_content.replace("helpline_number", config.CONTACT_NUMBER)
            
            message.attach(MIMEText(html_content, 'html'))
        except FileNotFoundError:
            logger.error(f"Template file not found at {config.TEMPLATE_FILE}")
            raise

        # Attach PDF if provided
        if attachment_path:
            try:
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition', 
                    f'attachment; filename="{attachment_path.name}"'
                )
                message.attach(part)
            except Exception as e:
                logger.error(f"Failed to attach {attachment_path.name}: {e}")

        return message

    def send_batch(self, recipients: list, attachment_path=None) -> int:
        """
        Sends an email to a list of recipients. 
        Returns the number of successful sends.
        """
        if not self.server:
            logger.error("Attempted to send batch without an active SMTP connection.")
            raise ConnectionError("SMTP server is not connected.")

        success_count = 0
        for recipient in recipients:
            try:
                msg = self._build_message(recipient, attachment_path)
                self.server.sendmail(self.sender_email, recipient, msg.as_string())
                success_count += 1
            except Exception as e:
                logger.error(f"Failed to send to {recipient}: {e}")
                # We do not break the loop here; one failed recipient shouldn't stop the whole batch.
        
        return success_count
