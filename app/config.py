import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-123')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///instance/database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # WhatsApp Config
    WHATSAPP_TOKEN = os.environ.get('WHATSAPP_TOKEN')
    WHATSAPP_PHONE_NUMBER_ID = os.environ.get('WHATSAPP_PHONE_NUMBER_ID')
    WHATSAPP_VERIFY_TOKEN = os.environ.get('WHATSAPP_VERIFY_TOKEN')
    
    # API Keys
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
    XAI_API_KEY = os.environ.get('XAI_API_KEY')
    
    # Pinecone Config
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
    PINECONE_ENVIRONMENT = os.environ.get('PINECONE_ENVIRONMENT')
    PINECONE_INDEX_NAME = os.environ.get('PINECONE_INDEX_NAME', 'whatsapp-rag')
