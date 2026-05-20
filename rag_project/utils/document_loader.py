import logging
from typing import List, Any
from PyPDF2 import PdfReader
from langchain_core.documents import Document

logger = logging.getLogger(__name__)

def process_uploaded_files(uploaded_files: List[Any]) -> List[Document]:
    """
    Processes a list of Streamlit UploadedFile objects and extracts text into LangChain Document objects.
    This exists to decouple Streamlit's binary object behavior from the abstract natural language models.
    Without this, models couldn't automatically read from raw user uploads.

    Args:
        uploaded_files (List[Any]): List of uploaded file objects.

    Returns:
        List[Document]: List of documents representing the text from each uploaded file.

    Example:
        >>> process_uploaded_files([<streamlit_file_object>])
        [Document(page_content="...")]
    """
    documents = []
    
    for file in uploaded_files:
        try:
            # We process different file types based on lowercase extension logic
            file_extension = file.name.split(".")[-1].lower()
            text = ""
            
            if file_extension == "pdf":
                pdf_reader = PdfReader(file)
                # Loop through pages iteratively extracting strings
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                        
            elif file_extension == "txt":
                # Convert straight bytes into UTF-8 standard text
                text = file.getvalue().decode("utf-8")
                
            else:
                logger.warning(f"Skipping unsupported file type: {file.name}")
                continue
                
            if text.strip():
                # Store text along with source metadata for critical citations later on
                doc = Document(page_content=text, metadata={"source": file.name})
                documents.append(doc)
                logger.info(f"Successfully loaded document: {file.name}")
            else:
                logger.warning(f"No text extracted from file: {file.name}")
                
        except Exception as e:
            logger.error(f"Error processing file {file.name}: {e}")
            raise RuntimeError(f"Failed to extract readable text from: {file.name}") from e
            
    return documents
