import streamlit as st
import os
import config
from utils.validator import validate_file_extension
from utils.document_loader import process_uploaded_files
from utils.chunker import chunk_documents
from utils.embedder import create_vector_store, load_vector_store
from utils.retriever import generate_answer

def main() -> None:
    """
    Core entrypoint initialization for the RAG architecture stack.
    Handles HTML Streamlit manipulation mapped against API limits and File IO bindings.
    Exists to bind the user layer directly up to the LLM backend cleanly.
    
    Example:
        `streamlit run app.py` bootstraps localhost 8501
    """
    # System meta title
    st.set_page_config(page_title="DocMinds", page_icon="📖", layout="wide")
    
    st.title("DocMinds - Multi-Document RAG Research Assistant")
    st.markdown("Upload academic PDFs or TXTs, generate embeddings, and pose research queries safely without hallucination.")

    # UI Left Navigation Component Block
    with st.sidebar:

        uploaded_files = st.file_uploader(
            "Upload your structured PDF or TXT files", 
            accept_multiple_files=True,
            type=config.SUPPORTED_FILE_TYPES
        )
        
        # Trigger Execution Event
        if st.button("Initialize & Process Documents"):
            if not config.check_keys():
                st.error("SYSTEM HALT: Missing Google API Key in bounds of .env configuration file.")
                return
                
            if not uploaded_files:
                st.error("Input missing. Please upload at least one system document.")
                return
            
            # Additional rigorous internal validation blocking
            for f in uploaded_files:
                if not validate_file_extension(f.name):
                    st.error(f"Security constraint caught block. Unsupported format: {f.name}")
                    return

            # Visual spinning progress logic to manage user expectation
            with st.spinner("Abstracting token mapping into dense vector representations..."):
                try:
                    # Ingestion Stage Execution
                    st.info("Parsing logical structures...")
                    docs = process_uploaded_files(uploaded_files)
                    
                    if not docs:
                        st.error("No valid text could be extracted from your files. If it's a scanned PDF, it may require OCR.")
                        return
                    
                    # Split Stage Execution
                    st.info("Recursive text segmenting execution...")
                    chunks = chunk_documents(docs)
                    
                    if not chunks:
                        st.error("Text segmentation resulted in zero chunks. The files might be unreadable or empty.")
                        return
                    
                    # Store Stage Execution
                    st.info("FAISS Matrix binding in active execution...")
                    create_vector_store(chunks)
                    
                    st.success("Embedding architecture synchronized. System clear for logical Queries.")
                except Exception as e:
                    # Traps standard errors preventing raw red-screen traces showing to user
                    st.error(f"Internal subsystem critical execution failure: {str(e)}")

    # UI Center Output Component Block

    
    # Store chat logic sequentially across Streamlit reloads 
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Re-draw the entire local history tree on state change reload loops
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    db_exists = os.path.exists(config.DB_FAISS_PATH)
    query = st.chat_input(
        "Ask a research question about your documents..." if db_exists else "Please process documents in the sidebar to enable chat.",
        disabled=not db_exists
    )
    
    if query:
        # Halt execution on empty edge cases gracefully
        if not query.strip():
            st.warning("Please enter a valid question.")
            return
            
        if not config.check_keys():
            st.error("SYSTEM HALT: Critical API Key credentials absent.")
            return

        # Explicit check preventing K=4 retrieval failure on blank FAISS arrays
        if not db_exists:
            st.warning("Vector Store missing. Please process files on the System Sidebar first before asking questions.")
            return

        # Echo human logic string visually
        with st.chat_message("user"):
            st.markdown(query)
            
        st.session_state.messages.append({"role": "user", "content": query})

        # Process Machine generative response graphically
        with st.chat_message("assistant"):
            with st.spinner("Decoding internal FAISS indexes against model endpoint API limits..."):
                try:
                    # Execute load cycle protocol logic manually inside request scope
                    vector_store = load_vector_store()
                    
                    # Retrieve the mapped logic
                    result = generate_answer(query, vector_store)
                    answer = result.get("answer", "System returned logically Null.")
                    source_docs = result.get("context", [])
                    
                    # Clean abstract Citations matching unique source sets 
                    citations = set()
                    for doc in source_docs:
                        if doc.metadata and "source" in doc.metadata:
                            citations.add(doc.metadata["source"])
                            
                    citation_text = ""
                    if citations:
                        citation_text = "\n\n**Explicit Context Identifiers:**\n" + "\n".join([f"- {source}" for source in citations])
                        
                    # Bind answer string logic combined with internal citations
                    full_response = answer + citation_text
                    
                    st.markdown(full_response)
                    
                    # Build IO Export logical stream bindings natively for user extraction
                    st.download_button(
                        label="Data File Output Download Engine",
                        data=full_response,
                        file_name="assistant_data_stream.txt",
                        mime="text/plain"
                    )
                    
                    # Overwrite state buffer mapping iteratively 
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                except Exception as e:
                    st.error(f"Failed querying local FAISS matrix store abstraction layers: {str(e)}")

# Bind entry execution tree execution limit bounds
if __name__ == "__main__":
    main()
