"""
B2B Sales Intelligence
Intent Classification & Prioritization Layer

This sanitized portfolio implementation demonstrates how a
commercial signal can be classified and prioritized using
structured business rules.

The public version intentionally avoids production APIs,
private datasets, client-specific configurations, and
operational infrastructure.

The classification layer is designed to support human sales
judgment rather than replace it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class IntentResult:
    """
    Result of commercial intent evaluation.
    """

    category: str
    base_score: int
    keyword_bonus: int
    persona_bonus: int
    final_score: int
    priority: str
    rationale: str


# Base intent scores.
#
# Higher scores represent stronger commercial signals.
INTENT_SCORES = {
    "Buying Request": 85,
    "Recommendation": 80,
    "Hiring": 75,
    "Business Challenge": 70,
    "General Discussion": 30,
}


# Simplified keyword groups used only to demonstrate
# the classification methodology.
INTENT_KEYWORDS = {
    "Buying Request": [
        "looking for",
        "need a provider",
        "seeking",
        "require support",
        "need help",
    ],
    "Recommendation": [
        "recommend",
        "recommendation",
        "suggest a vendor",
        "who can help",
        "any recommendations",
    ],
    "Hiring": [
        "hiring",
        "looking to hire",
        "open position",
        "recruiting",
        "talent",
    ],
    "Business Challenge": [
        "challenge",
        "struggling with",
        "problem",
        "difficulty",
        "need to improve",
        "gap",
    ],
}


def normalize_text(text: str) -> str:
    """
    Normalize text before classification.
    """

    return " ".join(text.lower().split())


def detect_intent(
    text: str,
    explicit_category: Optional[str] = None,
) -> tuple[str, int, str]:
    """
    Determine the most likely commercial intent category.

    If an explicit category is supplied, it is used as the
    starting classification.

    Otherwise, the function evaluates simplified keyword
    patterns.

    Returns:
        category, base_score, rationale
    """

    normalized = normalize_text(text)

    if explicit_category in INTENT_SCORES:
        return (
            explicit_category,
            INTENT_SCORES[explicit_category],
            "Category supplied by the upstream signal-processing layer.",
        )

    best_category = "General Discussion"
    best_matches = 0

    for category, keywords in INTENT_KEYWORDS.items():
        matches = sum(
            1 for keyword in keywords
            if keyword in normalized
        )

        if matches > best_matches:
            best_matches = matches
            best_category = category

    rationale = (
        f"Detected {best_matches} matching commercial signal pattern(s)."
        if best_matches
        else "No strong commercial intent pattern was detected."
    )

    return (
        best_category,
        INTENT_SCORES[best_category],
        rationale,
    )


def calculate_keyword_bonus(
    text: str,
    category: str,
    maximum_bonus: int = 10,
) -> int:
    """
    Calculate a small keyword-strength bonus.

    The bonus is intentionally capped so that keyword matches
    cannot overwhelm the underlying intent classification.
    """

    if category not in INTENT_KEYWORDS:
        return 0

    normalized = normalize_text(text)

    matches = sum(
        1
        for keyword in INTENT_KEYWORDS[category]
        if keyword in normalized
    )

    return min(matches * 5, maximum_bonus)


def calculate_persona_bonus(
    persona: Optional[str],
) -> int:
    """
    Apply a small bonus when the signal is associated with
    a potentially relevant business persona.
    """

    if not persona:
        return 0

    relevant_personas = {
        "business leader",
        "functional leader",
        "hr leader",
        "learning and development leader",
        "procurement stakeholder",
        "decision maker",
        "decision-maker",
    }

    normalized = persona.lower().strip()

    return 5 if normalized in relevant_personas else 0


def determine_priority(score: int) -> str:
    """
    Convert the final score into a practical priority category.

    The thresholds are intentionally simple and transparent.
    They are intended for prioritization, not guaranteed
    qualification.
    """

    if score >= 80:
        return "HOT"

    if score >= 70:
        return "WARM"

    if score >= 60:
        return "REVIEW"

    return "LOW PRIORITY"


def classify_signal(
    text: str,
    explicit_category: Optional[str] = None,
    persona: Optional[str] = None,
) -> IntentResult:
    """
    Run the complete intent evaluation process.

    Processing sequence:

        1. Intent classification
        2. Keyword-strength adjustment
        3. Buyer-persona adjustment
        4. Priority determination
    """

    category, base_score, rationale = detect_intent(
        text=text,
        explicit_category=explicit_category,
    )

    keyword_bonus = calculate_keyword_bonus(
        text=text,
        category=category,
    )

    persona_bonus = calculate_persona_bonus(
        persona=persona,
    )

    final_score = min(
        base_score + keyword_bonus + persona_bonus,
        100,
    )

    priority = determine_priority(final_score)

    return IntentResult(
        category=category,
        base_score=base_score,
        keyword_bonus=keyword_bonus,
        persona_bonus=persona_bonus,
        final_score=final_score,
        priority=priority,
        rationale=rationale,
    )


def evaluate_signal(
    text: str,
    persona: Optional[str] = None,
    explicit_category: Optional[str] = None,
) -> dict:
    """
    Produce a structured commercial-intelligence result.

    This output is designed to be consumed by a downstream
    human-review or sales workflow.
    """

    result = classify_signal(
        text=text,
        explicit_category=explicit_category,
        persona=persona,
    )

    return {
        "intent_category": result.category,
        "base_score": result.base_score,
        "keyword_bonus": result.keyword_bonus,
        "persona_bonus": result.persona_bonus,
        "final_score": result.final_score,
        "priority": result.priority,
        "rationale": result.rationale,
        "human_review_required": True,
    }


if __name__ == "__main__":
    demo_signal = (
        "Example Enterprise is looking for external support to "
        "improve leadership capability during a period of growth."
    )

    evaluation = evaluate_signal(
        text=demo_signal,
        persona="Business Leader",
    )

    print("B2B Sales Intelligence Demo")
    print("-" * 30)

    for key, value in evaluation.items():
        print(f"{key}: {value}")
