"""Formal evaluation metrics calculations for IKB-RAG.

Computes:
- Precision@k (proportion of top-k retrieved hits matching source_pages)
- Hit@k (binary: is at least one relevant page in top-k)
- MRR (Mean Reciprocal Rank of the first relevant page)
- Query Router Accuracy (predicted intent vs expected_intent)
- Citation Accuracy (presence of expected Page citation in output)
- Diagram Link Recall (presence of markdown image link when has_figure=True)
"""

from typing import List, Dict, Any, Union


def compute_precision_at_k(hits: List[Dict[str, Any]], target_pages: List[int], k: int = 5) -> float:
    """Computes Precision@k: fraction of top-k hits whose page_num is in target_pages."""
    if not hits or k <= 0:
        return 0.0
    top_k_hits = hits[:k]
    relevant_count = sum(1 for h in top_k_hits if h.get("page_num") in target_pages)
    return relevant_count / float(k)


def compute_hit_at_k(hits: List[Dict[str, Any]], target_pages: List[int], k: int = 5) -> float:
    """Computes Hit@k: 1.0 if any hit in top-k has page_num in target_pages, else 0.0."""
    top_k_hits = hits[:k]
    return 1.0 if any(h.get("page_num") in target_pages for h in top_k_hits) else 0.0


def compute_mrr(hits: List[Dict[str, Any]], target_pages: List[int]) -> float:
    """Computes Reciprocal Rank (RR): 1 / rank of first relevant hit (1-indexed)."""
    for rank, h in enumerate(hits, start=1):
        if h.get("page_num") in target_pages:
            return 1.0 / rank
    return 0.0


def evaluate_router_accuracy(predicted_intent: str, expected_intent: str) -> float:
    """Returns 1.0 if router intent prediction matches expected, else 0.0."""
    return 1.0 if predicted_intent.strip().upper() == expected_intent.strip().upper() else 0.0


def evaluate_citation_accuracy(answer: str, expected_citation: str) -> float:
    """Returns 1.0 if expected page citation appears in generated answer, else 0.0."""
    if not expected_citation:
        return 1.0
    return 1.0 if expected_citation.lower() in answer.lower() else 0.0


def evaluate_diagram_presence(answer: str, has_figure: bool) -> Union[float, None]:
    """Returns 1.0 if diagram markdown is present when has_figure=True, else 0.0."""
    if not has_figure:
        return None
    # Markdown image syntax check: ![...](...)
    has_md_img = "![" in answer and "](" in answer
    return 1.0 if has_md_img else 0.0
