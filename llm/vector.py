
# openai embeddings used
"""Contains logic to store and retrieve vectors (FAISS vector store)."""
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.config import logger


embedding_model = OpenAIEmbeddings()

def store_vector_store(documents, index_path="faiss_db_new"):
    """"
    Save the book content as chunks in vector database.
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunked_documents = text_splitter.split_documents(documents)
        faiss_db = FAISS.from_documents(chunked_documents, embedding_model)
        faiss_db.save_local(index_path)
        print("book stored in vector database")
    except Exception as error:
        logger.error(f"Error in saving vector data: {error}", exc_info=True)