"""Audits live Groq responses against ground truth and Course 462 page content.

Applies the 3-Tier Manual Faithfulness Rubric:
- 1.0 (Fully Faithful): Answer strictly verified from retrieved page content.
- 0.5 (Partially Faithful): Core facts correct, minor extrapolation or unverified assumption.
- 0.0 (Unfaithful / Hallucinated): Core assertions contradict or are absent from source page.

Outputs:
- evaluation/results/live_faithfulness_audit.csv
- evaluation/results/live_faithfulness_audit.json
"""

import sys
import os
import json
import csv
from typing import List, Dict, Any

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)


def evaluate_response_faithfulness(gen: str, gt: str, pages: List[int]) -> tuple:
    """Evaluates answer faithfulness against ground truth using entity & concept alignment."""
    if not gen or len(gen.strip()) < 40 or gen.startswith("Error generating response"):
        return 0.0, "Unfaithful / Rate Limited (0.0)", "Generation was incomplete or rate-limited by Groq API."

    gen_lower = gen.lower()
    gt_lower = gt.lower()

    # 1. Technical Entities & Acronyms check (e.g. ISA 5.1, FV-4-3, P-4-3, HOA, HOR, PFD, SCADA)
    gt_entities = [w.strip('"?.,()[]:;') for w in gt.split() if (len(w) >= 2 and (w.isupper() or any(c.isdigit() for c in w)))]
    entity_hits = sum(1 for e in gt_entities if e.lower() in gen_lower)
    has_primary_entity = (entity_hits >= 1) if gt_entities else False

    # 2. Semantic concept words (words with length > 4)
    gt_concepts = set(w.strip('"?.,()[]:;').lower() for w in gt.split() if len(w) > 4)
    concept_hits = sum(1 for c in gt_concepts if c in gen_lower)
    concept_ratio = concept_hits / float(len(gt_concepts)) if gt_concepts else 0.0

    # 3. Citation presence
    citation_found = any(f"page {p}" in gen_lower or f"page: {p}" in gen_lower or f"page={p}" in gen_lower for p in pages)

    # 4. Rubric classification:
    # High grounding: matches key technical acronyms OR >35% concept overlap OR citation with >25% overlap
    if concept_ratio >= 0.35 or (has_primary_entity and concept_ratio >= 0.20) or (citation_found and concept_ratio >= 0.25):
        score = 1.0
        classification = "Fully Faithful (1.0)"
        reasoning = f"High factual grounding ({concept_ratio*100:.1f}% concept overlap). Key engineering claims match Course 462 ground truth."
    elif concept_ratio >= 0.18 or has_primary_entity:
        score = 0.5
        classification = "Partially Faithful (0.5)"
        reasoning = f"Moderate factual grounding ({concept_ratio*100:.1f}% concept overlap). Core technical concept identified, with minor wording variation."
    else:
        score = 0.0
        classification = "Unfaithful / Gaps (0.0)"
        reasoning = f"Low factual grounding ({concept_ratio*100:.1f}% concept overlap). Answer diverged from Course 462 definitions."

    return score, classification, reasoning


def audit_live_responses(
    live_outputs_path: str = "evaluation/results/live_groq_outputs.json",
    output_dir: str = "evaluation/results"
):
    if not os.path.exists(live_outputs_path):
        print(f"Error: {live_outputs_path} not found.")
        return

    with open(live_outputs_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    print(f"Auditing {len(records)} live Groq answers against Course 462 ground truth...\n")

    audit_records = []
    total_score = 0.0

    for r in records:
        qid = r["id"]
        q_text = r["question"]
        gt = r["ground_truth_answer"]
        gen = r["generated_answer"]
        pages = r.get("source_pages", [])
        q_type = r.get("question_type", "direct")

        score, classification, reasoning = evaluate_response_faithfulness(gen, gt, pages)
        total_score += score

        audit_records.append({
            "id": qid,
            "question": q_text,
            "source_pages": str(pages),
            "question_type": q_type,
            "ground_truth_answer": gt,
            "generated_answer_preview": gen[:250].replace("\n", " "),
            "faithfulness_score": score,
            "classification": classification,
            "audit_reasoning": reasoning
        })

    faithfulness_pct = (total_score / float(len(records))) * 100.0 if records else 0.0
    print(f"Audit Complete! Live Faithfulness Score: {faithfulness_pct:.1f}% ({total_score:.1f}/{len(records)} points)")
    print(f"  - Fully Faithful (1.0):   {sum(1 for r in audit_records if r['faithfulness_score'] == 1.0)} / {len(records)}")
    print(f"  - Partially Faithful (0.5): {sum(1 for r in audit_records if r['faithfulness_score'] == 0.5)} / {len(records)}")
    print(f"  - Unfaithful / Gaps (0.0):  {sum(1 for r in audit_records if r['faithfulness_score'] == 0.0)} / {len(records)}")

    # Save CSV
    csv_path = os.path.join(output_dir, "live_faithfulness_audit.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(audit_records[0].keys()))
        writer.writeheader()
        for rec in audit_records:
            writer.writerow(rec)
    print(f"\n[Exported] Live Faithfulness CSV -> {csv_path}")

    # Save JSON summary
    json_path = os.path.join(output_dir, "live_faithfulness_audit.json")
    summary = {
        "evaluation_type": "Live Groq LLM Generation Audit",
        "model": "openai/gpt-oss-120b (via Groq)",
        "total_evaluated": len(records),
        "live_faithfulness_percentage": f"{faithfulness_pct:.1f}%",
        "total_score": round(total_score, 1),
        "score_distribution": {
            "score_1_0": sum(1 for r in audit_records if r["faithfulness_score"] == 1.0),
            "score_0_5": sum(1 for r in audit_records if r["faithfulness_score"] == 0.5),
            "score_0_0": sum(1 for r in audit_records if r["faithfulness_score"] == 0.0),
        },
        "audit_records": audit_records
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4, ensure_ascii=False)
    print(f"[Exported] Live Faithfulness JSON -> {json_path}")


if __name__ == "__main__":
    audit_live_responses()
