# MECHLEDGER

### Industrial Knowledge & Diagnostics

**Every machine has a history. Every diagnosis needs evidence.**

MECHLEDGER turns equipment manuals and maintenance documents into a source-linked diagnostic workspace. Engineers can index a PDF, provide verified asset context, describe a fault, inspect retrieved manual pages, and export the investigation as a PDF report.

The product builds on the open-source [IKB-RAG project](https://github.com/Abhishekirito/IKB-RAG). Its upstream README declares the project MIT licensed. The checked-out source does not contain a standalone `LICENSE` file; consult the upstream repository for the license text and inherited notices. The MECHLEDGER name and interface do not change the origin of the inherited backend and RAG code.

## What is implemented

- Simple chat workspace with browser-saved conversations, clear add-manual and delete-conversation controls, and per-file status.
- PDF, DOCX, and UTF-8 TXT uploads with extension, format, duplicate-name, and 50 MB size checks. Upload files are isolated by case identifier.
- MinerU service integration for document parsing. Uploads are saved immediately and processed in the background; if the remote reader times out, local text extraction is tried for text-based PDFs, DOCX, and TXT files.
- Failed files stay saved and can be retried from the manual list. Local PDF fallback preserves page numbers but does not extract diagrams or OCR scanned pages.
- Structural chunking with page context and source links, then local Ollama embeddings through its batch `/api/embed` endpoint.
- Qdrant vector search when configured, with a local JSON vector store fallback. Collections and local index files are scoped to the selected embedding model; existing indexes are not automatically deleted.
- Groq chat completion when a Groq key is configured. The current client also uses the configured local Ollama chat model when Groq is not configured or rejects a key.
- Evidence cautious response generation: no retrieved passages produces an explicit insufficient-evidence response; the answer prompt requires citations copied from retrieval context and separates hypotheses from documented facts.
- Citation links open the indexed PDF in the inspector at the cited page where the browser PDF viewer supports page fragments.
- Case-specific PDF maintenance reports with equipment fields, symptom, investigation messages, source file names, engineer remarks, and safety note.
- Case deletion removes that case's indexed data and stored documents through the existing backend lifecycle.
- The library reports whether each stored PDF has vectors for the active embedding model. Re-processing replaces a source's vectors only after parsing and embedding succeed, preserving the prior source vectors when either step fails.

## Architecture

```text
React / Vite
   │ upload, query, document, report APIs
   ▼
FastAPI ── MinerU parsing service
   │
   ├── Ollama /api/embed ── vectors ── Qdrant (optional)
   │                                  └─ local JSON fallback
   └── Groq Chat Completions (or configured local Ollama chat model)
```

For each question, the engine classifies query complexity, embeds one or more search queries, retrieves only the current case's indexed passages, groups matched elements with their source page context, and asks the generation model to answer using those passages. Equipment details entered in the interface are explicitly passed as operator-provided, unverified context. They do not become document evidence.

## Requirements

- Windows 10/11
- Python 3.10 or later
- Node.js 20.19+ or 22.12+ for the Vite 8 toolchain
- Ollama installed and running locally
- Access to the configured MinerU parsing service (the default endpoint is hosted)
- Optional: Groq API key for hosted generation
- Optional: Qdrant URL and API key for remote vector storage; without them the local JSON store is used

## Windows setup

From PowerShell in the repository root:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Install and start Ollama, then pull the embedding model:

```powershell
ollama pull nomic-embed-text
```

The configured embedding model is `nomic-embed-text`, which returns 768-dimensional vectors. To select another Ollama embedding model, set both `OLLAMA_EMBED_MODEL` and its actual `OLLAMA_EMBED_DIMENSION`. A new model selects a separate local index file and default Qdrant collection. Existing collections and data are left intact; use **Re-process stored PDFs** in Technical Library to build the new model's index. If a manually selected Qdrant collection has the wrong dimension, startup reports the mismatch instead of deleting it.

Set `GROQ_API_KEY` in `.env` for hosted response generation. Without it, pull the default local chat model:

```powershell
ollama pull qwen2.5:3b
```

The MinerU parser endpoint is configurable. Set `HF_TOKEN` if the configured service requires it. Keep credentials in the backend `.env`; Vite exposes no server secrets to the browser.

### Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama runtime URL |
| `OLLAMA_EMBED_MODEL` | `nomic-embed-text` | Local embedding model name |
| `OLLAMA_EMBED_DIMENSION` | `768` | Expected embedding dimension |
| `OLLAMA_CHAT_MODEL` | `qwen2.5:3b` | Local generation fallback model |
| `GROQ_API_KEY` | unset | Optional Groq API credential |
| `GROQ_MODEL` | `openai/gpt-oss-120b` | Groq generation model |
| `QDRANT_URL` | unset | Optional Qdrant server URL |
| `QDRANT_API_KEY` | unset | Optional Qdrant credential |
| `QDRANT_COLLECTION_NAME` | `mechledger-<embedding-model>` | Optional model-scoped collection override |
| `HF_TOKEN` | unset | Optional token for the MinerU service |
| `MINERU_API_URL` | configured hosted MinerU endpoint | Document parser endpoint |
| `MINERU_TIMEOUT_SECONDS` | `300` | Time limit for each remote document parse request |
| `MAX_UPLOAD_MB` | `50` | Maximum PDF upload size |

## Run the application

Start the FastAPI backend from the repository root:

```powershell
python api.py
```

The API listens at `http://localhost:8002`. Open a second PowerShell in `frontend`:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal. The API docs are at `http://localhost:8002/docs`.

## Demonstration workflow

1. Create or select a diagnostic case.
2. Choose **Add a manual** and wait until its status says **Ready**. If processing fails, choose **Retry** beside the file.
3. Describe the symptom, observed conditions, and checks already completed.
4. Review the answer and open its source links to check the relevant manual page.
5. Choose **Report** to download a PDF copy of the conversation.

Do not use generated output as an authorization to work. Verify source passages and follow the current controlled OEM documentation and site safety requirements.

## API overview

- `GET /` — service status
- `POST /upload` — multipart PDF, DOCX, or TXT upload (`chat_id`, `file`)
- `GET /documents?chat_id=…` — case document names
- `GET /documents/status?chat_id=…` — per-file index status for the configured embedding model
- `POST /documents/{chat_id}/{filename}/process` — retry a saved document
- `GET /documents/{chat_id}/{filename}` — source PDF
- `DELETE /documents/{chat_id}/{filename}` — remove one source PDF and its extracted evidence/vectors across MECHLEDGER model indexes
- `GET /images/{chat_id}/{pdf_base}/{filename}` — extracted image
- `POST /query` — question, case ID, and optional operator equipment context
- `POST /reports/{chat_id}` — generate a case PDF report from actual case data provided by the client
- `POST /chat/{chat_id}/refresh` — re-parse this case's stored PDFs
- `DELETE /chat/{chat_id}` — remove this case's vectors and files

## Tests and build

```powershell
python -m unittest discover -s tests -v
cd frontend
npm run build
```

The embedding tests mock Ollama responses; they validate batching and dimension checks without requiring a running Ollama service. Full document parsing and live answer generation require the configured MinerU service, Ollama models, and optionally Groq or Qdrant credentials.

## Current limitations

- The hosted MinerU parser is external. Saved files remain on the backend if it times out. Text-based PDFs, DOCX, and TXT files use a local text fallback; diagrams are omitted and scanned PDFs still require OCR.
- This checkout has no authentication or user accounts. Case IDs isolate app data paths and vector retrieval, but are not an access-control boundary for a multi-user deployment.
- Case titles, conversation history, and equipment fields are stored in the browser's local storage. The backend stores documents and vectors, not a durable case conversation database.
- The PDF report is a printable text-first summary; it does not reproduce MinerU diagrams or images, and source references are listed by document rather than embedded as clickable PDF links.
- PDF page navigation depends on browser PDF viewer support. Retrieved citations are generated from MinerU page indices and source links.
- MinerU may omit content or fail on malformed, scanned, or unusually complex PDFs; inspect the parser output and original document.
- Responses are not validated engineering findings. Always verify each claim against the referenced controlled manual.

## Upstream acknowledgement

MECHLEDGER preserves the IKB-RAG FastAPI, React/Vite, MinerU, retrieval, and vector-storage foundation and its declared MIT licensing. The application branding and evidence-focused workspace are a product transformation of that inherited codebase. See [Abhishekirito/IKB-RAG](https://github.com/Abhishekirito/IKB-RAG) for the upstream project and its license declaration.
