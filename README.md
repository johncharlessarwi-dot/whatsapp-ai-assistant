
---

# WhatsApp AI Assistant

> Production-ready WhatsApp AI Assistant powered by Retrieval-Augmented Generation (RAG), intelligent LLM routing, conversation memory, and document-based question answering.

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square\&logo=python\&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web_App-000000?style=flat-square\&logo=flask)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-1C3C3C?style=flat-square)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector_DB-4B2EFF?style=flat-square)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat-square\&logo=sqlite)

![WhatsApp](https://img.shields.io/badge/WhatsApp-Cloud_API-25D366?style=flat-square\&logo=whatsapp)
![Groq](https://img.shields.io/badge/Groq-Primary_LLM-F55036?style=flat-square)
![Gemini](https://img.shields.io/badge/Gemini-Fallback_LLM-4285F4?style=flat-square)
![OpenAI](https://img.shields.io/badge/OpenAI-Fallback_LLM-412991?style=flat-square\&logo=openai)
![Claude](https://img.shields.io/badge/Claude-Sonnet-D97757?style=flat-square)

![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square\&logo=docker)
![License](https://img.shields.io/github/license/cleven12/whatsapp-ai-assistant?style=flat-square)
![Stars](https://img.shields.io/github/stars/cleven12/whatsapp-ai-assistant?style=flat-square)

</p>

---

## Overview

WhatsApp AI Assistant is a scalable AI-powered customer support and knowledge assistant that enables users to interact with your organization directly through WhatsApp.

The system combines:

* Retrieval-Augmented Generation (RAG)
* Multi-provider LLM routing
* Vector search
* Conversation memory
* Document management dashboard
* WhatsApp Cloud API integration

to deliver accurate and cost-efficient responses grounded in your own knowledge base.

---

## Architecture

```mermaid
flowchart TD

A[WhatsApp User]

A --> B[WhatsApp Cloud API]

B --> C[Flask Backend]

C --> D[Conversation Memory]
C --> E[RAG Engine]

E --> F[Document Loader]
E --> G[Text Splitter]
E --> H[Pinecone Vector Database]

H --> I[Relevant Context]

I --> J[LLM Router]

J --> K[Groq]
J --> L[Gemini]
J --> M[OpenAI]
J --> N[Claude]
J --> O[xAI]

K --> P[Generated Response]
L --> P
M --> P
N --> P
O --> P

P --> B
B --> A
```

---

## Technology Stack

```mermaid
mindmap
  root((WhatsApp AI Assistant))

    Backend
      Flask
      Python
      LangChain

    Messaging
      WhatsApp Cloud API

    AI
      Groq
      Gemini
      OpenAI
      Claude
      xAI

    Retrieval
      Pinecone
      Embeddings
      RAG

    Storage
      SQLite

    Deployment
      Docker
      Linux
      Nginx
```

---

## Key Features

| Feature               | Description                               |
| --------------------- | ----------------------------------------- |
| RAG Search            | Answers generated from your own documents |
| WhatsApp Integration  | Native WhatsApp Cloud API support         |
| Multi-LLM Routing     | Automatic provider fallback               |
| Conversation Memory   | Maintains context across chats            |
| Document Management   | Upload and manage PDFs, TXT files         |
| Cost Optimization     | Uses lower-cost models first              |
| Docker Support        | Easy deployment                           |
| Scalable Architecture | Suitable for production workloads         |

---

## LLM Fallback Strategy

```mermaid
flowchart LR

A[User Query]

A --> B{Groq Available?}

B -->|Yes| C[Groq]

B -->|No| D{Gemini Available?}

D -->|Yes| E[Gemini]

D -->|No| F{OpenAI Available?}

F -->|Yes| G[OpenAI]

F -->|No| H{Claude Available?}

H -->|Yes| I[Claude]

H -->|No| J[xAI]

J --> K[Response]
I --> K
G --> K
E --> K
C --> K
```

---

## Project Structure

```text
whatsapp-ai-assistant/
│
├── app/
│   ├── routes/
│   ├── services/
│   ├── rag/
│   ├── llm/
│   ├── models/
│   └── templates/
│
├── uploads/
├── vector_store/
├── static/
│
├── docker/
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── app.py
```

---

## Request Processing Flow

```mermaid
sequenceDiagram

participant User
participant WhatsApp
participant Backend
participant Pinecone
participant LLM

User->>WhatsApp: Send message

WhatsApp->>Backend: Webhook event

Backend->>Pinecone: Retrieve context

Pinecone-->>Backend: Relevant documents

Backend->>LLM: Prompt + Context

LLM-->>Backend: AI response

Backend->>WhatsApp: Send response

WhatsApp->>User: Reply delivered
```

---

## Quick Start

```bash
git clone https://github.com/cleven12/whatsapp-ai-assistant.git

cd whatsapp-ai-assistant

cp .env.example .env

docker compose up --build
```
