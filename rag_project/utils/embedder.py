import os
import time
import logging
from typing import List, Optional
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import config

logger = logging.getLogger(__name__)

def create_vector_store(chunks: List[Document]) -> Optional[FAISS]:
    """
    Creates a FAISS vector store from document chunks and saves it locally.
    It exists to map physical human text into dense float vectors. 
    Without this, mathematical similarity queries couldn't be run by the retriever.

    Args:
        chunks (List[Document]): Document chunks to embed.

    Returns:
        Optional[FAISS]: FAISS vector store generated object.

    Example:
        >>> create_vector_store([Document(page_content="test")])
        <FAISS object>
    """
    try:
        # Prevent API calls if local environment is unsafe/missing credentials
        if not config.check_keys():
            raise ValueError("Google API key configuration missing.")
            
        embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)
        
        if not chunks:
            logger.warning("No chunks provided to embedder.")
            return None

        # Initialize and build FAISS vector store mapping texts to vectors locally
        logger.info(f"Generating embeddings locally using {config.EMBEDDING_MODEL_NAME}...")
        vector_store = FAISS.from_documents(chunks, embeddings)
        
        # Save locally to completely avoid rebilling the API limit on restarts
        os.makedirs(os.path.dirname(config.DB_FAISS_PATH), exist_ok=True)
        vector_store.save_local(config.DB_FAISS_PATH)
        
        logger.info("Successfully vectorized and saved local FAISS index.")
        return vector_store
        
    except ValueError as ve:
        logger.error(f"Configuration setup strictly prohibited API Call: {ve}")
        raise
    except Exception as e:
        logger.error(f"Deep neural matrix mapping failed: {e}")
        raise RuntimeError(f"Vector store processing was aborted: {str(e)}") from e
        
def load_vector_store() -> FAISS:
    """
    Loads an existing FAISS vector store directly from local physical disk bounds.
    Exists to retrieve our previously stored intelligence rather than start from scratch.

    Returns:
        FAISS: Loaded FAISS vector store mapping.

    Example:
        >>> load_vector_store()
        <FAISS object>
    """
    try:
        if not config.check_keys():
            raise ValueError("Credentials absent prior to embedding recall limit checks.")
            
        embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)
        # allow_dangerous_deserialization=True is critically required in FAISS 1.8.x + to load local OS safe pickle bytes
        vector_store = FAISS.load_local(config.DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
        logger.info("Local FAISS matrices rehydrated properly.")
        return vector_store
        
    except Exception as e:
        logger.error(f"Failed to unpickle local vector files: {e}")
        raise RuntimeError(f"Vector disk block failure on {config.DB_FAISS_PATH}.") from e
