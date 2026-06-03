from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore as LangChainPinecone
from langchain_huggingface import HuggingFaceEmbeddings
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.api_key = current_app.config['PINECONE_API_KEY']
        self.index_name = current_app.config['PINECONE_INDEX_NAME']
        
        # Using a free/cheap embedding model
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        self.pc = Pinecone(api_key=self.api_key)
        self.index = self.pc.Index(self.index_name)

    def query(self, text, k=3):
        """
        Query Pinecone for relevant context.
        """
        try:
            vectorstore = LangChainPinecone(
                self.index, 
                self.embeddings, 
                "text"
            )
            docs = vectorstore.similarity_search(text, k=k)
            return "\n".join([doc.page_content for doc in docs])
        except Exception as e:
            logger.error(f"Error querying Pinecone: {e}")
            return ""
