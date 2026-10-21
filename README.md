<div align="center">

# 🏭 IKB-RAG
### Industrial Knowledge Base powered by Retrieval-Augmented Generation (RAG)

<p align="center">
An AI-powered Industrial Troubleshooting Assistant built for engineers, maintenance teams, and manufacturing industries.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=FFD62E)
![Qdrant](https://img.shields.io/badge/Qdrant-FF4F8B?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-000000?style=for-the-badge)
![MIT License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</p>

---

### 📚 Built With

FastAPI • React • Vite • Groq • Qdrant Cloud • MinerU • Nomic Embeddings • Hugging Face Spaces

</div>

---

# 📖 Table of Contents

- [📌 Overview](#overview)
- [🚀 Live Demo](#live-demo)
- [✨ Key Features](#key-features)
- [🏗️ Architecture](#architecture)
- [⚙️ Tech Stack](#tech-stack)
- [📁 Project Structure](#project-structure)
- [🚀 Getting Started](#getting-started)
- [🔑 Environment Variables](#environment-variables)
- [📦 Install Backend](#install-backend)
- [▶️ Start Backend](#start-backend)
- [💻 Frontend Installation](#frontend-installation)
- [🚦 Application Workflow](#application-workflow)
- [🌟 Highlights](#highlights)
- [🌐 Backend API](#backend-api)
- [🧠 RAG Pipeline](#rag-pipeline)
- [🔒 AI Guardrails](#ai-guardrails)
- [💻 Frontend Features](#frontend-features)
- [☁️ Hugging Face Microservices](#hugging-face-microservices)
- [📊 Performance Highlights](#performance-highlights)
- [📈 Roadmap](#roadmap)
- [🤝 Contributing](#contributing)
- [📜 License](#license)
- [💡 Future Vision](#future-vision)
- [🙌 Acknowledgements](#acknowledgements)

---

<h1 id="overview">📌 Overview</h1>

IKB-RAG is a full-stack AI-powered Industrial Knowledge Assistant that combines Retrieval-Augmented Generation (RAG) with multimodal document understanding to help engineers diagnose industrial equipment failures quickly and accurately.

Unlike traditional chatbots, IKB-RAG understands:

- 📄 Industrial manuals
- 📊 Tables
- 📈 Technical diagrams
- 🧮 Mathematical formulas
- 📝 Maintenance reports

using **MinerU's multimodal parsing engine**, stores document embeddings inside **Qdrant Cloud**, and generates contextual expert responses through **Groq's Llama 3 models**.

The result is an intelligent troubleshooting assistant capable of delivering highly accurate answers with precise document citations.

---

<h1 id="live-demo">🚀 Live Demo</h1>

Experience IKB-RAG in action through the live application and interactive walkthrough.

<div align="center">

&nbsp;

<a href="https://youtu.be/A2U511YVBXA">
  <img src="https://img.shields.io/badge/▶️%20Watch%20Demo-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube Demo">
</a>

</div>

<br>

<p align="center">
  <a href="https://youtu.be/A2U511YVBXA">
    <img src="assets/1.png" width="900" alt="IKB-RAG Demo">
  </a>
</p>

<p align="center">
<b>👆 Click the thumbnail above to watch the complete project walkthrough.</b>
</p>


## ✨ What You'll See

- 📄 Upload and parse industrial PDF manuals
- 🔍 Semantic document retrieval using RAG
- 🤖 AI-powered troubleshooting with Groq Llama 3
- 📑 Source-aware responses with page citations
- 🖼️ Automatic extraction of tables, diagrams, and images
- ☁️ Persistent vector storage using Qdrant Cloud
- 🎨 Modern glassmorphism-based user interface

---

<h1 id="key-features">✨ Key Features</h1>

## 🤖 AI Powered Troubleshooting

- Industrial domain-specific RAG pipeline
- Root Cause Analysis (RCA)
- Equipment diagnostics
- Context-aware answers
- Expert-level troubleshooting

---

## 📄 Intelligent PDF Processing

✔ OCR

✔ Tables

✔ Mathematical equations

✔ Engineering diagrams

✔ Layout detection

✔ Structured document parsing

Powered by **MinerU**

---

## 🔎 Semantic Search

- Vector embeddings
- Parent Document Retrieval
- Context reconstruction
- Citation-aware responses
- Exact page references

---

## ☁ Cloud Native

- Qdrant Cloud
- Hugging Face Spaces
- Stateless backend
- Scalable architecture
- Persistent vector storage

---

## 🎨 Modern User Interface

- Glassmorphism design
- Animated upload pipeline
- Built-in PDF viewer
- Responsive layout
- Interactive chat experience

---

<h1 id="architecture">🏗️ Architecture</h1>

<img src="assets/3.png" width="900" alt="IKB-RAG Architecture">

---

<h1 id="tech-stack">⚙️ Tech Stack</h1>

| Category | Technologies |
|-----------|--------------|
| Frontend | React, Vite |
| Backend | FastAPI |
| Vector Database | Qdrant Cloud |
| Embeddings | Nomic Embed Text v1.5 |
| LLM | Groq Llama 3 |
| PDF Parsing | MinerU |
| Hosting | Hugging Face Spaces |
| Language | Python |
| Styling | CSS Glassmorphism |

---

<h1 id="project-structure">📁 Project Structure</h1>

```text
IKB-RAG
│
├── api/                       # Modular FastAPI application layer
│   ├── main.py                # FastAPI app initialization & CORS middleware
│   ├── routes.py              # Endpoints (/query, /upload, /documents, /images, etc.)
│   └── schemas.py             # Pydantic request models
│
├── config/                    # Centralized settings & configurations
│   └── settings.py            # Environment variables, API keys, models, and paths
│
├── src/ikb_rag/               # Core Industrial RAG Pipeline Package
│   ├── ingestion/             # Document loading (MinerU) & structural element chunking
│   │   ├── loaders.py
│   │   └── chunking.py
│   ├── embeddings/            # Vector embedding generators (Nomic Atlas)
│   │   └── embedder.py
│   ├── vectorstore/           # Vector databases & index lifecycle management
│   │   ├── qdrant_store.py    # Qdrant Cloud integration
│   │   ├── simple_json_store.py # Local JSON fallback & pure-Python cosine similarity
│   │   └── index_manager.py   # Re-indexing, deletion, and storage cleaning
│   ├── retrieval/             # Query transformation & context retrieval
│   │   ├── query_transforms.py # Intent router (SIMPLE/COMPLEX) & QA decomposer
│   │   └── retriever.py       # Similarity retrieval & parent-document context assembly
│   ├── generation/            # Prompt templates & LLM synthesis
│   │   ├── prompt_templates.py # Industrial RCA Copilot & query prompts
│   │   ├── llm_client.py      # Groq Llama-3 client wrapper
│   │   └── response_generator.py # Formats context & generates expert answers
│   ├── pipeline/              # Orchestration layer
│   │   └── rag_pipeline.py    # IKBRagEngine & singleton rag_engine
│   └── utils/                 # Filesystem & storage utility helpers
│       └── file_utils.py
│
├── scripts/                   # CLI entrypoints
│   ├── run_query.py           # Test queries directly from terminal
│   └── build_index.py         # Index manuals directly from terminal
│
├── tests/                     # Unit and integration test suite
│   ├── test_imports.py
│   └── test_components.py
│
├── frontend/                  # React + Vite Frontend application
│   ├── src/App.jsx            # Core UI, Chat Interface, PDF Viewer
│   └── src/index.css          # Glassmorphism aesthetic tokens
│
├── uploaded_documents/        # Local cache of active manuals
├── static_images/             # High-res P&IDs and diagrams extracted by MinerU
├── parsed_data/               # MinerU JSON & Markdown artifacts
│
├── archive/                   # Preserved original pre-refactor backups
│   ├── legacy_pikerag_rag_utils_backup.py
│   └── legacy_api_backup.py
│
├── .env
├── README.md
├── api.py                     # Root launcher (backward compatible: python api.py)
└── requirements.txt
```


---

<h1 id="getting-started">🚀 Getting Started</h1>

## Prerequisites

Before running the project, make sure you have installed:

- Python 3.10+
- Node.js 18+
- npm
- Git

You will also need API keys for:

- Hugging Face
- Groq
- Nomic
- Qdrant Cloud

---

<h1 id="environment-variables">🔑 Environment Variables</h1>

Create a `.env` file in the root directory.

```env
HF_TOKEN=your_huggingface_token

GROQ_API_KEY=your_groq_api_key

NOMIC_API_KEY=your_nomic_api_key

QDRANT_URL=https://your-cluster-url.cloud.qdrant.io:6333

QDRANT_API_KEY=your_qdrant_api_key
```

---

<h1 id="install-backend">📦 Install Backend</h1>

```bash
pip install fastapi

pip install uvicorn

pip install python-multipart

pip install requests

pip install groq

pip install qdrant-client

pip install python-dotenv
```

or simply

```bash
pip install -r requirements.txt
```

---

<h1 id="start-backend">▶️ Start Backend</h1>

```bash
python api.py
```

When the backend starts, it automatically performs a diagnostic health check:

- ✅ Groq Connection
- ✅ Hugging Face API
- ✅ Qdrant Database
- ✅ Environment Variables

Backend URL

```
http://localhost:8002
```

---

<h1 id="frontend-installation">💻 Frontend Installation</h1>

Open a new terminal.

```bash
cd frontend
```

Install packages

```bash
npm install
```

Start development server

```bash
npm run dev
```

Frontend URL

```
http://localhost:5173
```

---

<h1 id="application-workflow">🚦 Application Workflow</h1>

```text
Start Backend
      │
      ▼
Start Frontend
      │
      ▼
Upload PDF
      │
      ▼
MinerU extracts document
      │
      ▼
Embeddings generated
      │
      ▼
Stored inside Qdrant
      │
      ▼
Ask Questions
      │
      ▼
Relevant Context Retrieved
      │
      ▼
Groq Generates Final Answer
```

---

<h1 id="highlights">🌟 Highlights</h1>

- ⚡ Low latency responses
- 📄 Accurate document citations
- 🧠 Parent Document Retrieval
- ☁ Fully cloud scalable
- 🔒 Secure session isolation
- 📊 Engineering-focused responses
- 🎨 Modern responsive UI

---

<h1 id="backend-api">🌐 Backend API</h1>

The FastAPI backend exposes a clean REST API responsible for document management, vector indexing, retrieval, and chat lifecycle management.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|----------|----------|-------------|
| POST | `/upload` | Uploads a PDF, extracts its contents, generates embeddings, and indexes them into Qdrant. |
| GET | `/documents` | Retrieves all uploaded documents for a chat session. |
| GET | `/documents/{chat_id}/{filename}` | Opens the original uploaded PDF. |
| GET | `/images/{chat_id}/{pdf_base}/{filename}` | Serves extracted engineering diagrams and images. |
| POST | `/query` | Accepts user queries and streams AI-generated responses. |
| POST | `/chat/{chat_id}/refresh` | Re-indexes all uploaded documents. |
| DELETE | `/chat/{chat_id}` | Permanently deletes all chat data, vectors, images, and uploaded files. |

---

## 🔄 API Workflow

```text
Client
   │
   ▼
FastAPI
   │
   ├── Upload PDF
   ├── Extract Content
   ├── Generate Embeddings
   ├── Store in Qdrant
   └── Return Status

Query Request
      │
      ▼
Retrieve Relevant Chunks
      │
      ▼
Groq LLM
      │
      ▼
Streaming Response
```

---

<h1 id="rag-pipeline">🧠 RAG Pipeline</h1>

The Retrieval-Augmented Generation pipeline is designed specifically for industrial documentation, where preserving structure and context is essential.

---

## 📄 Step 1 — Document Parsing

Every uploaded PDF is processed by **MinerU**, which extracts:

- 📄 Paragraphs
- 📊 Tables
- 📈 Engineering Charts
- 🖼 Diagrams
- 🧮 Mathematical Formulae
- 📑 Document Layout
- 🔤 OCR Text

Unlike traditional PDF parsers, MinerU preserves the structural hierarchy of technical documents.

---

## ✂ Step 2 — Intelligent Chunking

Instead of splitting documents by arbitrary token limits, the engine separates content based on structural elements.

Each chunk represents:

- One paragraph
- One table
- One image
- One formula
- One engineering block

This significantly improves retrieval precision.

---

## 🧬 Step 3 — Embedding Generation

Each extracted chunk is converted into a high-dimensional vector using:

**Nomic Embed Text v1.5**

Benefits include:

- Semantic similarity
- Fast vector search
- Context preservation
- High retrieval accuracy

---

## ☁ Step 4 — Vector Storage

Embeddings are stored inside **Qdrant Cloud**.

Each vector stores:

- Chat ID
- PDF filename
- Page number
- Chunk type
- Source citation
- Metadata

This enables efficient filtering and scalable search.

---

## 🔎 Step 5 — Semantic Retrieval

When a question is asked:

1. Generate query embedding
2. Search nearest vectors
3. Retrieve highest-scoring chunks
4. Reconstruct surrounding context
5. Send enriched prompt to Groq

---

## 🧩 Parent Document Retrieval

Instead of sending isolated chunks to the LLM, the engine retrieves the surrounding page or section to provide additional context.

Benefits:

- Better reasoning
- Reduced hallucinations
- Improved engineering accuracy
- More natural answers

---

## 🤖 Step 6 — LLM Response Generation

Groq's Llama 3 model receives:

- User question
- Retrieved context
- Source metadata
- Industrial system prompt

The model generates an expert-level troubleshooting response while maintaining strict industrial guardrails.

---

<h1 id="ai-guardrails">🔒 AI Guardrails</h1>

The assistant is intentionally restricted to industrial engineering domains.

It will:

✅ Explain industrial equipment

✅ Analyze manuals

✅ Diagnose failures

✅ Provide maintenance guidance

✅ Perform Root Cause Analysis

It refuses:

❌ General knowledge

❌ Casual conversations

❌ Irrelevant programming queries

❌ Off-topic requests

unless directly related to industrial systems.

---

<h1 id="frontend-features">💻 Frontend Features</h1>

The frontend is built using **React + Vite** with a modern glassmorphism interface.

---

## 🎨 User Experience

### ✨ Glassmorphism Design

- Frosted panels
- Gradient accents
- Soft shadows
- Blur effects
- Smooth animations

---

### 📂 Interactive Upload Experience

Instead of a loading spinner, users see a live processing pipeline showing:

```
Uploading PDF...

Parsing Layout...

Extracting Tables...

Extracting Images...

Generating Embeddings...

Uploading to Qdrant...

Ready!
```

---

### 📑 Integrated PDF Viewer

Features:

- Open original PDF
- Jump directly to cited page
- Side-by-side reading
- Source verification

---

### 💬 AI Chat Interface

Features include:

- Streaming responses
- Markdown rendering
- Code blocks
- Hyperlinks
- PDF citations
- Image references

---

### 🗑 Safe Chat Management

Includes elegant confirmation dialogs before:

- Deleting chats
- Removing documents
- Clearing vector database

---

<h1 id="hugging-face-microservices">☁️ Hugging Face Microservices</h1>

Heavy computation is outsourced to Hugging Face Spaces, keeping deployment lightweight.

---

## 📄 MinerU Service

Responsible for:

- OCR
- Layout detection
- Table extraction
- Image extraction
- Formula recognition

Input:

```
PDF
```

Output:

```
content_list.json
images/
metadata
```

---

## 🧬 Nomic Embedding Service

Responsible for generating semantic embeddings.

Advantages:

- Fast
- Cloud-hosted
- GPU accelerated
- Highly accurate

---

<h1 id="performance-highlights">📊 Performance Highlights</h1>

| Feature | Benefit |
|----------|----------|
| Parent Retrieval | Better context |
| Cloud Vectors | Scalable search |
| Streaming LLM | Low latency |
| MinerU Parsing | Rich document understanding |
| Glass UI | Excellent UX |
| Session Isolation | Secure multi-user support |


---

<h1 id="roadmap">📈 Roadmap</h1>

## ✅ Completed

- PDF Upload
- MinerU Integration
- Vector Search
- Groq Integration
- Glassmorphism UI
- Citation Navigation

---

## 🚧 In Progress

- Multi-document reasoning
- Conversation memory
- Authentication
- User dashboard
- Search history

---

## 🔮 Planned

- Voice Assistant
- Mobile App
- OCR for Images
- Knowledge Graph
- Local LLM Deployment
- Docker Deployment
- Kubernetes Support

---

<h1 id="contributing">🤝 Contributing</h1>

Contributions are welcome!

### Steps

```bash
Fork Repository

Clone Repository

Create Feature Branch

Commit Changes

Push Branch

Create Pull Request
```

---

<h1 id="license">📜 License</h1>

This project is licensed under the **MIT License**.

Feel free to use, modify, and distribute this project under the terms of the license.

---

<h1 id="future-vision">💡 Future Vision</h1>

IKB-RAG aims to become a complete AI-powered Industrial Knowledge Platform capable of assisting engineers throughout the equipment lifecycle - from installation and maintenance to diagnostics, predictive analytics, and intelligent documentation search.

Future enhancements will focus on expanding multimodal understanding, improving collaboration features, and integrating with enterprise systems.

---

<h1 id="acknowledgements">🙌 Acknowledgements</h1>

Special thanks to the amazing open-source community and technologies powering this project.

❤️ FastAPI

⚛ React

⚡ Vite

🧠 Groq

📄 MinerU

☁ Hugging Face

📦 Qdrant

🧬 Nomic AI

---

<div align="center">

## ⭐ If you found this project useful...

Give it a ⭐ on GitHub and consider contributing!

Made with ❤️ for Industrial AI, Manufacturing, and Engineering Innovation.

---

**IKB-RAG — Industrial Knowledge Base powered by Retrieval-Augmented Generation**

</div>
