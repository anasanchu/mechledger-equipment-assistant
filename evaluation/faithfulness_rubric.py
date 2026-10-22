"""Manual Faithfulness Rubric and Audit Methodology for IKB-RAG.

Faithfulness Rubric Standard:
-----------------------------
Evaluates whether every factual claim in the generated answer is strictly
grounded in the retrieved parent-document context (no hallucinations or
unsubstantiated domain extrapolation).

Scoring Scale:
- 1.0 (Faithful): Every factual statement is explicitly confirmed by the retrieved context.
- 0.5 (Partially Faithful): The primary answer is correct and supported, but contains a
  minor unverified inference, phrasing assumption, or domain generalization.
- 0.0 (Unfaithful / Hallucinated): The answer contains equipment codes, functional
  descriptions, or operational logic that directly contradict the retrieved context or
  cannot be verified from the retrieved context.

Faithfulness Score Formula:
    Faithfulness % = (Sum of scores across N questions) / N * 100
"""

from typing import Dict, Any, List


class FaithfulnessAuditor:
    """Provides structured auditing rules and worksheet generation for manual faithfulness grading."""

    RUBRIC_CRITERIA = {
        1.0: "Fully Faithful: All statements are explicitly verified by retrieved context.",
        0.5: "Partially Faithful: Core facts verified; minor unsupported inference or generalization.",
        0.0: "Unfaithful: Assertions contradict context or equipment tags/functions are hallucinated."
    }

    @staticmethod
    def audit_entry(
        question_id: str,
        question: str,
        ground_truth: str,
        retrieved_context: str,
        generated_answer: str,
        score: float,
        reasoning: str
    ) -> Dict[str, Any]:
        """Creates a standardized audit record for the faithfulness worksheet."""
        return {
            "id": question_id,
            "question": question,
            "ground_truth": ground_truth,
            "retrieved_context_summary": retrieved_context[:300] + ("..." if len(retrieved_context) > 300 else ""),
            "generated_answer": generated_answer,
            "faithfulness_score": score,
            "audit_rubric_classification": FaithfulnessAuditor.RUBRIC_CRITERIA.get(score, "Custom"),
            "audit_reasoning": reasoning
        }
