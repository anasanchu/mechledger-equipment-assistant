"""Live end-to-end question answering runner on Groq LLM with smart TPM retry.

Executes all 50 questions from golden_set.json through the real IKB-RAG pipeline:
- Query Transformer (Intent Router / Decomposer)
- Retriever (Parent-Document Retrieval via Qdrant)
- Response Generator (Groq LLM)

Features:
- Validates each generated response (retries on 'Error generating response' or 429 TPM errors).
- 12s token recovery sleep between successful queries to stay under the 8,000 TPM limit.
- Incremental autosaving: updates evaluation/results/live_groq_outputs.json after every success.
- Automatically skips the 15 already verified queries.
"""

import sys
import os
import json
import time
from typing import List, Dict, Any

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

from src.ikb_rag.pipeline.rag_pipeline import IKBRagEngine


def load_golden_set(filepath: str = "evaluation/golden_set/golden_set.json") -> List[Dict[str, Any]]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("golden_set", [])


def load_existing_valid_outputs(filepath: str = "evaluation/results/live_groq_outputs.json") -> Dict[str, Dict[str, Any]]:
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Only keep genuine completed answers (filter out error responses)
            valid = {}
            for item in data:
                ans = item.get("generated_answer", "")
                if ans and not ans.startswith("Error generating response") and len(ans) > 40:
                    valid[item["id"]] = item
            return valid
    except Exception:
        return {}


def save_outputs(outputs: List[Dict[str, Any]], filepath: str = "evaluation/results/live_groq_outputs.json"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(outputs, f, indent=4, ensure_ascii=False)


def main():
    print("=" * 60, flush=True)
    print(" [*] RESUMING LIVE RAG GENERATION ON GROQ (SMART TPM PACING)", flush=True)
    print("=" * 60, flush=True)

    output_path = "evaluation/results/live_groq_outputs.json"
    questions = load_golden_set()
    completed_map = load_existing_valid_outputs(output_path)

    print(f"Total Golden Set Questions: {len(questions)}", flush=True)
    print(f"Already Verified Valid Answers: {len(completed_map)}/50", flush=True)
    remaining_count = len(questions) - len(completed_map)
    print(f"Remaining Questions to Generate: {remaining_count}\n", flush=True)

    engine = IKBRagEngine()

    # Preserve order of questions in final list
    for idx, q in enumerate(questions, start=1):
        qid = q["id"]
        q_text = q["question"]

        if qid in completed_map:
            print(f"[{idx}/50] (Already Verified) {qid}: '{q_text[:45]}...'", flush=True)
            continue

        print(f"\n[{idx}/50] Generating {qid}: '{q_text}'", flush=True)

        max_retries = 6
        success = False
        answer = ""
        latency = 0.0

        for attempt in range(1, max_retries + 1):
            t0 = time.time()
            try:
                answer = engine.query(q_text, chat_id="1")
                latency = time.time() - t0

                is_valid = answer and not answer.startswith("Error generating response") and len(answer) > 40
                if is_valid:
                    success = True
                    print(f"  -> Success! Generated in {latency:.2f}s | Length: {len(answer)} chars", flush=True)
                    print(f"  -> Preview: {answer[:130].replace(chr(10), ' ')}...", flush=True)
                    break
                else:
                    print(f"  [Attempt {attempt}/{max_retries}] TPM limit reached. Waiting 14s for token bucket to reset...", flush=True)
                    time.sleep(14.0)

            except Exception as e:
                print(f"  [Attempt {attempt}/{max_retries}] Exception: {e}. Waiting 14s...", flush=True)
                time.sleep(14.0)

        if success:
            record = {
                "id": qid,
                "question": q_text,
                "ground_truth_answer": q["ground_truth_answer"],
                "source_file": q.get("source_file", "P&ID_DEMO.pdf"),
                "source_pages": q.get("source_pages", [q.get("source_page")]),
                "question_type": q.get("question_type", "direct"),
                "expected_intent": q.get("expected_intent", "SIMPLE"),
                "generated_answer": answer,
                "latency_seconds": round(latency, 2),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            completed_map[qid] = record

            # Re-compile full list preserving question order
            all_sorted = [completed_map[q_item["id"]] for q_item in questions if q_item["id"] in completed_map]
            save_outputs(all_sorted, output_path)
            print(f"  -> Saved! Progress: {len(completed_map)}/50 questions complete.", flush=True)

            # Wait 12 seconds between questions to maintain healthy token capacity
            if len(completed_map) < len(questions):
                print("  -> Token pacing: Sleeping 12s before next question...", flush=True)
                time.sleep(12.0)
        else:
            print(f"  [FAILED] Could not generate valid answer for {qid} after {max_retries} retries.", flush=True)

    print("\n" + "=" * 60, flush=True)
    print(f" [COMPLETED] LIVE GENERATION FINISHED: {len(completed_map)}/50 VERIFIED", flush=True)
    print(f" [SAVED] -> {output_path}", flush=True)
    print("=" * 60, flush=True)


if __name__ == "__main__":
    main()
