import pandas as pd
import logging
from pathlib import Path

from logger import setup_logger

logger = setup_logger()

class ContactManager:
    def __init__(self, contacts_path: Path, senders_path: Path):
        self.contacts_path = contacts_path
        self.senders_path = senders_path
        
        self.contacts_df = self._load_csv(self.contacts_path)
        self.senders_df = self._load_csv(self.senders_path)
        
        self._validate_data()

    def _load_csv(self, path: Path) -> pd.DataFrame:
        """Loads a CSV file into a Pandas DataFrame safely."""
        try:
            return pd.read_csv(path)
        except FileNotFoundError:
            logger.critical(f"Required data file missing: {path}")
            raise
        except pd.errors.EmptyDataError:
            logger.warning(f"Data file is empty: {path}")
            return pd.DataFrame()

    def _validate_data(self):
        """Ensures the required columns exist in the loaded DataFrames."""
        if not self.contacts_df.empty and 'Email' not in self.contacts_df.columns:
            raise ValueError(f"'Email' column missing in {self.contacts_path.name}")
        
        if not self.senders_df.empty:
            required_sender_cols = {'Email', 'pass'}
            if not required_sender_cols.issubset(self.senders_df.columns):
                raise ValueError(f"Required columns {required_sender_cols} missing in {self.senders_path.name}")

    def get_senders(self) -> pd.DataFrame:
        """Returns the DataFrame of sender accounts and passwords."""
        return self.senders_df

    def has_contacts(self) -> bool:
        """Checks if there are still contacts left to process."""
        return not self.contacts_df.empty

    def get_remaining_contacts_count(self) -> int:
        """Returns the total number of contacts left in the queue."""
        return len(self.contacts_df)

    def get_contact_batch(self, batch_size: int) -> list:
        """
        Retrieves the next batch of email addresses up to the specified batch_size.
        """
        if self.contacts_df.empty:
            return []
        
        batch_df = self.contacts_df.head(batch_size)
        return batch_df['Email'].tolist()

    def remove_processed_contacts(self, processed_emails: list):
        """
        Removes the given emails from the active DataFrame and updates the CSV file 
        to ensure they are not emailed again if the script restarts.
        """
        if not processed_emails:
            return

        # Filter out the processed emails from the active dataframe
        self.contacts_df = self.contacts_df[~self.contacts_df['Email'].isin(processed_emails)]
        
        # Save the updated state back to the disk
        try:
            self.contacts_df.to_csv(self.contacts_path, index=False)
            logger.debug(f"Removed {len(processed_emails)} processed contacts from {self.contacts_path.name}.")
        except PermissionError:
            logger.error(f"Permission denied: Could not save updates to {self.contacts_path.name}. Is the file open?")
        except Exception as e:
            logger.error(f"Failed to update {self.contacts_path.name}: {e}")
