import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

# Load environment variables
load_dotenv()

def ingest_docs():
    # 1. Configuration
    api_key = os.getenv('PINECONE_API_KEY')
    index_name = os.getenv('PINECONE_INDEX_NAME', 'whatsapp-rag')
    
    if not api_key:
        print("Error: PINECONE_API_KEY not found in .env")
        return

    print(f"Starting ingestion to index: {index_name}...")

    # 2. Load Documents from 'uploads' folder
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
        print("Created 'uploads' directory. Please put your .txt or .pdf files there.")
        return

    # Load TXT files
    loader_txt = DirectoryLoader('uploads/', glob="**/*.txt", loader_cls=TextLoader)
    # Load PDF files
    loader_pdf = DirectoryLoader('uploads/', glob="**/*.pdf", loader_cls=PyPDFLoader)
    
    docs = loader_txt.load() + loader_pdf.load()
    
    if not docs:
        print("No documents found in 'uploads/' directory.")
        return

    print(f"Loaded {len(docs)} documents.")

    # 3. Split Documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")

    # 4. Initialize Embeddings (Matching retriever.py)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 5. Push to Pinecone
    try:
        # Initialize Pinecone to check if index exists
        pc = Pinecone(api_key=api_key)
        
        # Check if index exists
        active_indexes = [index.name for index in pc.list_indexes()]
        if index_name not in active_indexes:
            print(f"Error: Index '{index_name}' does not exist in Pinecone.")
            print(f"Available indexes: {active_indexes}")
            return

        print("Uploading to Pinecone...")
        PineconeVectorStore.from_documents(
            chunks,
            embeddings,
            index_name=index_name
        )
        print("Successfully uploaded knowledge base to Pinecone!")

    except Exception as e:
        print(f"Error during ingestion: {e}")

if __name__ == "__main__":
    ingest_docs()
