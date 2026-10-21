"""CLI utility to index a document into the IKB-RAG vector store.

Usage:
    python scripts/build_index.py --file path/to/manual.pdf --chat-id "default"
"""

import sys
import os
import argparse

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ikb_rag import rag_engine


def main():
    parser = argparse.ArgumentParser(description="Index a document into the IKB-RAG vector database.")
    parser.add_argument("--file", "-f", type=str, required=True, help="Path to document file (PDF, DOCX, TXT)")
    parser.add_argument("--chat-id", "-c", type=str, default="default", help="Chat session ID (default: 'default')")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"[ERROR] File does not exist: {args.file}")
        sys.exit(1)

    print(f"\n[CLI] Indexing document '{args.file}' for chat '{args.chat_id}'...")
    num_chunks = rag_engine.index_document(args.file, chat_id=args.chat_id)
    print(f"[CLI] Successfully indexed {num_chunks} chunks.")


if __name__ == "__main__":
    main()
