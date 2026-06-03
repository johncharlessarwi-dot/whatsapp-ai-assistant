from flask import Blueprint, request, jsonify, current_app
from app.services.whatsapp import WhatsAppService
from app.llm.router import LLMRouter
from app.rag.retriever import RAGService
from app.models import User, Message
from app import db
import logging

webhook_bp = Blueprint('webhook', __name__)
logger = logging.getLogger(__name__)

@webhook_bp.route('/', methods=['GET'], strict_slashes=False)
def verify():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode and token:
        if mode == 'subscribe' and token == current_app.config['WHATSAPP_VERIFY_TOKEN']:
            return challenge, 200
        else:
            return 'Forbidden', 403
    return 'Bad Request', 400

@webhook_bp.route('/', methods=['POST'], strict_slashes=False)
def handle_message():
    data = request.get_json()
    
    # Check if it's a valid WhatsApp message
    if not data or 'entry' not in data:
        return jsonify({"status": "ignored"}), 200

    try:
        entry = data['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        
        if 'messages' in value:
            message_obj = value['messages'][0]
            whatsapp_number = message_obj['from']
            
            if 'text' in message_obj:
                user_text = message_obj['text']['body']
                process_user_message(whatsapp_number, user_text)
            
    except Exception as e:
        logger.error(f"Error parsing webhook: {e}")

    return jsonify({"status": "success"}), 200

def process_user_message(whatsapp_number, user_text):
    """
    Core logic for RAG + LLM + Memory
    """
    # 1. Get or Create User
    user = User.query.filter_by(whatsapp_number=whatsapp_number).first()
    if not user:
        user = User(whatsapp_number=whatsapp_number)
        db.session.add(user)
        db.session.commit()

    # 2. Save User Message
    user_msg = Message(user_id=user.id, role='user', content=user_text)
    db.session.add(user_msg)
    
    # 3. Retrieve Context from RAG
    rag_service = RAGService()
    context = rag_service.query(user_text)
    
    # 4. Get LLM and Generate Response
    llm_router = LLMRouter()
    llm = llm_router.get_llm()
    
    # Fetch recent conversation history (last 5 messages)
    history = Message.query.filter_by(user_id=user.id).order_by(Message.timestamp.desc()).limit(5).all()
    history_text = "\n".join([f"{m.role}: {m.content}" for m in reversed(history)])

    prompt = f"""You are a helpful AI assistant. Use the following context to answer the user's question. 
    If you don't know the answer, say you don't know based on the provided documents.
    
    Context:
    {context}
    
    Conversation History:
    {history_text}
    
    User Question: {user_text}
    """
    
    try:
        response = llm.invoke(prompt)
        ai_text = response.content
    except Exception as e:
        logger.error(f"LLM Invocation error: {e}")
        ai_text = "I'm sorry, I'm having trouble processing your request right now."

    # 5. Save Assistant Message
    assistant_msg = Message(user_id=user.id, role='assistant', content=ai_text)
    db.session.add(assistant_msg)
    db.session.commit()

    # 6. Send Response via WhatsApp
    whatsapp_service = WhatsAppService()
    whatsapp_service.send_message(whatsapp_number, ai_text)
