import logging
from typing import Dict, Any
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import config

logger = logging.getLogger(__name__)

def generate_answer(query: str, vector_store: FAISS) -> Dict[str, Any]:
    """
    Retrieves strict context bounds from vector store and uses LLM memory mapping to reply.
    It exists to connect the human's abstract query, through a search algorithm, into a generative text output.
    Without this file, you have no intelligence to reason over what you found.

    Args:
        query (str): The logical human question.
        vector_store (FAISS): Indexed embedding logic bounds mapping.

    Returns:
        Dict[str, Any]: Mapping holding the "answer" text and the internal source "context" documents mapping.

    Example:
        >>> generate_answer("Explain theory of relativity.", db)
        {'answer': 'It states...', 'context': [<Doc A>, <Doc B>]}
    """
    try:
        # LLM instance initialized securely at runtime
        llm = ChatGoogleGenerativeAI(model=config.LLM_MODEL_NAME, temperature=0.3)
        
        # Hard lock system prompt to prevent Hallucination - major issue in standard ChatGPT
        system_prompt = (
            "You are a helpful and concise Academic Research Assistant. "
            "Use the provided context to heavily answer the exact user's question. "
            "If the exact answer is strictly not in the context shown, explicitly declare that you do not know. "
            "Do strictly avoid hallucinating external unproven facts. "
            "Context Source: {context}"
        )
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        
        # Build the RAG abstraction flow (Chain)
        question_answer_chain = create_stuff_documents_chain(llm, prompt_template)
        
        # k=4 means it will pull only the 4 mathematically closest paragraphs
        retriever = vector_store.as_retriever(search_kwargs={"k": 4})
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        logger.info(f"Issuing RAG Protocol generation block, snippet: {query[:40]}")
        
        # Fire chain execution blocking state sequentially
        response = rag_chain.invoke({"input": query})
        
        logger.info("Successfully unparsed LLM outputs and matched mapping contexts.")
        return response
        
    except Exception as e:
        logger.error(f"Inference Engine failed to resolve tokens: {e}")
        raise RuntimeError("Failure communicating over prompt mapping API boundaries.") from e
