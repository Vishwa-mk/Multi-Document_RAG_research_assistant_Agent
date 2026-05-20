import logging
import config

logger = logging.getLogger(__name__)

def validate_file_extension(filename: str) -> bool:
    """
    Validates if a file extension exists safely within white-listed limits.
    Exists to prevent zero-day exploit file types or corrupt binary formats.
    Without this, users could upload .exe or .sh breaking security limits.

    Args:
        filename (str): Target disk string checking.

    Returns:
        bool: Safety check passed.

    Example:
        >>> validate_file_extension("manual.pdf")
        True
    """
    try:
        # Basic sanity parse logic based upon splitting periods implicitly handling standard files
        extension = filename.split(".")[-1].lower()
        if extension in config.SUPPORTED_FILE_TYPES:
            logger.info(f"Validation Layer: Input {filename} verified.")
            return True
        logger.warning(f"Validation Layer Triggered: File {filename} denied access limit.")
        return False
    except Exception as e:
        logger.error(f"Validator logic failed edge case string: {e}")
        return False
