from flask import Blueprint, request, jsonify, current_app
from app.services.whatsapp import WhatsAppService
from app.llm.router import LLMRouter
from app.rag.retriever import RAGService
from app.models import User, Message
from app import db
import logging
import os
import json
from app.utils.webhook_security import verify_meta_signature
from app.utils.message_policy import validate_inbound_text
from app.utils.webhook_events import extract_text_events
from app.utils.phone import normalize_recipient
from app.utils.subscription import verify_subscription

webhook_bp = Blueprint('webhook', __name__)
logger = logging.getLogger(__name__)

@webhook_bp.route('/', methods=['GET'], strict_slashes=False)
def verify():
    status, body = verify_subscription(
        request.args.get('hub.mode'),
        request.args.get('hub.verify_token'),
        request.args.get('hub.challenge'),
        current_app.config.get('WHATSAPP_VERIFY_TOKEN'),
    )
    return body, status

@webhook_bp.route('/', methods=['POST'], strict_slashes=False)
def handle_message():
    # Verify the exact raw bytes before parsing JSON or invoking any external service.
    # Cap the stream read itself, including chunked requests without Content-Length.
    raw = request.stream.read(64 * 1024 + 1)
    if len(raw) > 64 * 1024:
        return jsonify({"error": "payload_too_large"}), 413
    signature = request.headers.get("X-Hub-Signature-256")
    if not verify_meta_signature(raw, signature, os.environ.get("META_APP_SECRET")):
        return jsonify({"error": "invalid_signature"}), 403

    try:
        data = json.loads(raw)
    except (UnicodeDecodeError, ValueError):
        return jsonify({"error": "invalid_json"}), 400
    if not isinstance(data, dict):
        return jsonify({"error": "invalid_json"}), 400

    for number, body in extract_text_events(data):
        try:
            safe_number = normalize_recipient(number)
            safe_text = validate_inbound_text(body)
            process_user_message(safe_number, safe_text)
        except ValueError:
            logger.warning("Rejected malformed WhatsApp text event")
        except Exception:
            db.session.rollback()
            logger.exception("WhatsApp text event processing failed")
            return jsonify({"error": "processing_failed"}), 503

    return jsonify({"status": "accepted"}), 200

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
