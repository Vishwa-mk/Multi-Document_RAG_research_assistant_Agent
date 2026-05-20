import logging
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import config

logger = logging.getLogger(__name__)

def chunk_documents(documents: List[Document]) -> List[Document]:
    """
    Splits a list of documents into smaller meaningful chunks for embeddings.
    Exists because LLMs have context limits and embedding whole books causes vector dilution.
    Without this, indexing would fail on large books or responses would dilute matching accuracy.

    Args:
        documents (List[Document]): The list of full-text documents.

    Returns:
        List[Document]: A list of chunked documents aligned with maximum token arrays.

    Example:
        >>> chunk_documents([Document(page_content="long text...")])
        [Document(page_content="long t..."), Document(page_content="...ext...")]
    """
    try:
        # Use RecursiveCharacterTextSplitter for optimal natural language chunking
        # Automatically tests splitting over Paragraphs (\n\n) then lines (\n)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Successfully split {len(documents)} documents into {len(chunks)} chunks.")
        
        return chunks
    
    except Exception as e:
        logger.error(f"Error during semantic chunking: {e}")
        raise RuntimeError("Mathematical chunking algorithm failed to split strings.") from e
