import os
import time
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

def setup_pinecone():
    api_key = os.getenv('PINECONE_API_KEY')
    index_name = os.getenv('PINECONE_INDEX_NAME', 'whatsapp-rag')
    
    if not api_key:
        print("Error: PINECONE_API_KEY missing.")
        return

    pc = Pinecone(api_key=api_key)

    # Check if index exists
    if index_name not in [index.name for index in pc.list_indexes()]:
        print(f"Index '{index_name}' not found. Creating it now...")
        try:
            pc.create_index(
                name=index_name,
                dimension=384, # Dimension for all-MiniLM-L6-v2
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
            print(f"Index '{index_name}' creation initiated.")
            
            # Wait for index to be ready
            while not pc.describe_index(index_name).status['ready']:
                time.sleep(1)
            print(f"Index '{index_name}' is ready!")
        except Exception as e:
            print(f"Error creating index: {e}")
    else:
        print(f"Index '{index_name}' already exists.")

if __name__ == "__main__":
    setup_pinecone()
