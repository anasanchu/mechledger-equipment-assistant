"""CLI utility to test a query against the IKB-RAG pipeline.

Usage:
    python scripts/run_query.py --question "How to troubleshoot pump vibration?" --chat-id "default"
"""

import sys
import os
import argparse

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ikb_rag import rag_engine


def main():
    parser = argparse.ArgumentParser(description="Query the IKB-RAG system from command line.")
    parser.add_argument("--question", "-q", type=str, required=True, help="Question to ask the Industrial Copilot")
    parser.add_argument("--chat-id", "-c", type=str, default="default", help="Chat session ID (default: 'default')")
    args = parser.parse_args()

    print(f"\n[CLI] Querying IKB-RAG (Chat ID: {args.chat_id})...")
    print(f"[CLI] Question: {args.question}\n")
    
    answer = rag_engine.query(args.question, chat_id=args.chat_id)
    print("\n" + "=" * 50)
    print("ANSWER:")
    print("=" * 50)
    print(answer)
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
