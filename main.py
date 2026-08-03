import sys
import logging
import config
from logger import setup_logger, log_campaign_metrics
from contacts import ContactManager
from mailer import SMTPClient
from utils import get_latest_attachment

def run_campaign():
    """
    Main orchestrator for the mass email campaign. 
    Handles sender rotation, batch processing, and error handling.
    """
    # 1. Initialize System Logger
    logger = setup_logger()
    logger.info("Starting mass email campaign orchestrator...")

    # 2. Initialize Contact Manager
    try:
        contact_manager = ContactManager(config.CONTACTS_FILE, config.SENDER_FILE)
        senders = contact_manager.get_senders()
        total_contacts = contact_manager.get_remaining_contacts_count()
        logger.info(f"Loaded {len(senders)} sender accounts and {total_contacts} target contacts.")
    except Exception as e:
        logger.critical(f"Failed to load data files: {e}")
        sys.exit(1)

    if total_contacts == 0:
        logger.warning("No contacts found in the database. Exiting.")
        sys.exit(0)

    # 3. Locate Attachment (if any)
    latest_attachment = get_latest_attachment(config.ATTACHMENT_DIR)
    if latest_attachment:
        logger.info(f"Will attach file: {latest_attachment.name}")
    else:
        logger.warning("No PDF attachments found in the attachments directory. Proceeding without attachments.")

    # 4. Campaign Execution Loop
    total_emails_sent = 0
    sender_index = 0

    while contact_manager.has_contacts():
        if sender_index >= len(senders):
            logger.error("All sender accounts have been exhausted or blocked.")
            break

        current_sender = senders.iloc[sender_index]
        sender_email = current_sender['Email']
        sender_password = current_sender['pass']

        logger.info(f"Authenticating sender account: {sender_email}")
        
        # Initialize SMTP Client for the current sender
        smtp_client = SMTPClient(sender_email, sender_password)
        
        if not smtp_client.connect():
            logger.warning(f"Failed to authenticate {sender_email}. Rotating to next sender.")
            sender_index += 1
            continue

        # Process batches using the current authenticated sender
        try:
            while contact_manager.has_contacts():
                batch = contact_manager.get_contact_batch(config.BATCH_SIZE)
                
                # Attempt to send the batch
                success_count = smtp_client.send_batch(batch, latest_attachment)
                total_emails_sent += success_count

                # Remove successful sends from the active queue to prevent duplicates
                contact_manager.remove_processed_contacts(batch)

                logger.info(f"Batch processed. {success_count}/{len(batch)} successful. Total sent: {total_emails_sent}")

        except Exception as e:
            # Catch SMTP limit exceptions or connection drops
            logger.error(f"Sender {sender_email} encountered an error: {e}. Rotating account.")
            sender_index += 1
        finally:
            smtp_client.disconnect()

    # 5. Final Reporting
    logger.info("Campaign completed or halted.")
    log_campaign_metrics(total_emails_sent)


if __name__ == "__main__":
    try:
        run_campaign()
    except KeyboardInterrupt:
        print("\nCampaign manually interrupted by user. Exiting gracefully...")
        sys.exit(0)
    except Exception as fatal_error:
        print(f"\nFATAL ERROR: {fatal_error}")
        sys.exit(1)
