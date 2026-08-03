from pathlib import Path
from logger import setup_logger

logger = setup_logger()

def get_latest_attachment(directory: Path, extension: str = '.pdf'):
    """
    Scans the given directory for files with the specified extension and 
    returns the path to the most recently modified file.
    Returns None if no files are found.
    """
    if not directory.exists() or not directory.is_dir():
        logger.error(f"Attachment directory does not exist or is invalid: {directory}")
        return None

    # Gather all files matching the extension
    files = list(directory.glob(f"*{extension}"))
    
    if not files:
        logger.debug(f"No {extension} files found in {directory.name}.")
        return None

    # Find the file with the most recent modification time
    try:
        latest_file = max(files, key=lambda f: f.stat().st_mtime)
        logger.info(f"Found latest attachment: {latest_file.name}")
        return latest_file
    except Exception as e:
        logger.error(f"Error while retrieving the latest attachment: {e}")
        return None
