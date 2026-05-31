# WhatsApp AI Assistant 🤖

> A smart, cost-efficient WhatsApp AI agent with RAG (Retrieval-Augmented Generation) capabilities. Answers questions based on your documents using powerful LLMs with intelligent fallback routing.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-4B2EFF?style=for-the-badge&logo=pinecone&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-FF6600?style=for-the-badge&logo=groq&logoColor=white)

![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

---

### Features

- **RAG-powered** answers from your uploaded documents (PDFs, TXT, etc.)
- **Smart LLM Fallback System**: Groq → Gemini → OpenAI → xAI → Claude Sonnet (budget-friendly)
- WhatsApp Cloud API integration
- Simple web dashboard for document management
- Conversation memory per user
- Fully Docker ready

### Quick Start

```bash
git clone https://github.com/cleven12/whatsapp-ai-assistant.git
cd whatsapp-ai-assistant
cp .env.example .env