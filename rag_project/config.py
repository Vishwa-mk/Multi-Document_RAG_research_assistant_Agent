import os
import logging
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup basic logging to monitor background processes
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# --- Constants ---
# Kept in config.py to avoid hardcoding inside business logic.
CHUNK_SIZE: int = 1000
CHUNK_OVERLAP: int = 200
EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
LLM_MODEL_NAME: str = "gemini-flash-latest"
DB_FAISS_PATH: str = "vectorstore/db_faiss"
SUPPORTED_FILE_TYPES: List[str] = ["pdf", "txt"]

def check_keys() -> bool:
    """
    Checks if all required API keys are present in the environment variables.

    Returns:
        bool: True if key exists and is not the default template string, False otherwise.
        
    Example:
        >>> check_keys()
        True
    """
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        # Ensure it's not None, empty, or the example placeholder.
        if not api_key or api_key == "your_google_api_key_here":
            return False
        return True
    except Exception as e:
        logging.error(f"Failed to check environment variables: {e}")
        return False
