**Architecture & Data Flow**

<img width="2086" height="786" alt="mermaid-drawing" src="https://github.com/user-attachments/assets/79082b75-c96a-4c9a-9faf-e7ffaeb33174" />


**Technologies used**
**Python** → Backend logic
**Streamlit** → Frontend (user interface)
**RAG (Retrieval-Augmented Generation)** → Core concept
**LLM (AI Model)** → To generate answers 


****Data Flow Execution Steps****
**1. **Upload Phase**: User transmits file buffer bindings through the UI.
2. **Load Engine Logic**: `process_uploaded_files` strictly pulls bytes over binary blocks turning them into LangChain Document native classes string bindings. 
3. **Chunk Segmentation**: `RecursiveCharacterTextSplitter` breaks lengthy NLP sequences mapping across 1000 threshold blocks to enforce token size restrictions.
4. **Embedding Stage**: Chunk arrays hit the local `HuggingFaceEmbeddings` model (`all-MiniLM-L6-v2`) transforming language semantics into deep floating-point numbers mapping arrays before persisting back out onto the FAISS mapped DB. This avoids restrictive cloud API rate limits while maintaining high semantic accuracy.
5. **Retrieval**: Natural queries index search mathematically picking out the top "K=4" nearest vectors avoiding iterating across blank space matrices. 
6. **LLM Synthesis**: Filtered matrix returns are merged inside the prompt alongside the question sending to `gemini-1.5-flash` forming absolute factual summaries.
7. **Delivery**: The synthesized AI string maps and extracts original filenames formatting exact block citations back over Streamlit outputs limits.


<img width="1919" height="1037" alt="Screenshot 2026-05-01 121747" src="https://github.com/user-attachments/assets/97f92eef-53b8-4de6-a84d-504578b62445" />
