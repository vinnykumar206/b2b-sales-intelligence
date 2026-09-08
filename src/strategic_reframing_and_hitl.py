"""
B2B Sales Intelligence
Strategic Reframing & Human-in-the-Loop Layer

This sanitized portfolio implementation demonstrates how a
prioritized commercial signal can be converted into a structured
sales-review brief.

The system does not automatically decide whether outreach should
occur. It prepares context and possible next actions for a human
sales professional.

Production-specific messaging, CRM integrations, credentials,
client information, and private datasets are intentionally excluded.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class SalesSignal:
    """
    Structured representation of a prioritized commercial signal.
    """

    organization: str
    signal_summary: str
    intent_category: str
    priority: str
    score: int
    buyer_persona: Optional[str] = None
    business_fit: Optional[str] = None
    source_type: Optional[str] = None


@dataclass
class SalesReviewBrief:
    """
    Human-review package generated from a commercial signal.
    """

    organization: str
    why_it_matters: str
    commercial_context: str
    possible_next_actions: list[str]
    recommended_review_action: str
    human_review_required: bool


def generate_why_it_matters(signal: SalesSignal) -> str:
    """
    Explain why a signal may deserve sales attention.

    The explanation is intentionally conservative. It describes
    potential relevance rather than claiming that the signal is
    a confirmed sales opportunity.
    """

    parts = []

    if signal.intent_category:
        parts.append(
            f"The signal has been classified as "
            f"'{signal.intent_category}'."
        )

    if signal.business_fit:
        parts.append(
            f"Business fit is currently assessed as "
            f"'{signal.business_fit}'."
        )

    if signal.buyer_persona:
        parts.append(
            f"A potentially relevant persona has been identified: "
            f"{signal.buyer_persona}."
        )

    parts.append(
        f"The current prioritization score is {signal.score}/100 "
        f"with a '{signal.priority}' priority."
    )

    return " ".join(parts)


def generate_commercial_context(signal: SalesSignal) -> str:
    """
    Convert the structured signal into a concise commercial context.

    The function deliberately avoids inventing facts that are not
    contained in the signal.
    """

    context = (
        f"Organization: {signal.organization}. "
        f"Signal: {signal.signal_summary}"
    )

    if signal.source_type:
        context += f" Source type: {signal.source_type}."

    return context


def generate_possible_actions(
    signal: SalesSignal,
) -> list[str]:
    """
    Generate human-review actions based on signal priority.

    These are options for a salesperson, not autonomous commands.
    """

    if signal.priority == "HOT":
        return [
            "Validate the original signal",
            "Research the account context",
            "Confirm stakeholder relevance",
            "Assess whether timely outreach is appropriate",
        ]

    if signal.priority == "WARM":
        return [
            "Validate the original signal",
            "Research the account further",
            "Confirm stakeholder relevance",
            "Consider follow-up research before outreach",
        ]

    if signal.priority == "REVIEW":
        return [
            "Review the signal manually",
            "Determine whether additional context is required",
            "Reassess commercial relevance",
        ]

    return [
        "Review only if additional context suggests relevance",
        "Defer or reject if commercial relevance remains weak",
    ]


def determine_review_action(
    signal: SalesSignal,
) -> str:
    """
    Recommend the next review step without making the final
    commercial decision.
    """

    if signal.priority == "HOT":
        return "Prioritize for human validation"

    if signal.priority == "WARM":
        return "Review for potential follow-up"

    if signal.priority == "REVIEW":
        return "Conduct additional research"

    return "Deprioritize unless new information emerges"


def create_review_brief(
    signal: SalesSignal,
) -> SalesReviewBrief:
    """
    Create a structured human-review brief.
    """

    return SalesReviewBrief(
        organization=signal.organization,
        why_it_matters=generate_why_it_matters(signal),
        commercial_context=generate_commercial_context(signal),
        possible_next_actions=generate_possible_actions(signal),
        recommended_review_action=determine_review_action(signal),
        human_review_required=True,
    )


def format_review_brief(
    brief: SalesReviewBrief,
) -> str:
    """
    Format the review brief for a human sales professional.
    """

    actions = "\n".join(
        f"- {action}"
        for action in brief.possible_next_actions
    )

    return (
        f"SALES INTELLIGENCE REVIEW\n"
        f"{'=' * 28}\n\n"
        f"Organization:\n"
        f"{brief.organization}\n\n"
        f"Why It May Matter:\n"
        f"{brief.why_it_matters}\n\n"
        f"Commercial Context:\n"
        f"{brief.commercial_context}\n\n"
        f"Possible Next Actions:\n"
        f"{actions}\n\n"
        f"Recommended Review Step:\n"
        f"{brief.recommended_review_action}\n\n"
        f"Human Review Required:\n"
        f"{brief.human_review_required}"
    )


def process_for_human_review(
    signal: SalesSignal,
) -> str:
    """
    Convert a prioritized signal into a human-reviewable brief.

    This function intentionally ends at human review.
    """

    brief = create_review_brief(signal)

    return format_review_brief(brief)


if __name__ == "__main__":
    demo_signal = SalesSignal(
        organization="Example Enterprise",
        signal_summary=(
            "Leadership publicly discusses the need to improve "
            "leadership capability during organizational growth."
        ),
        intent_category="Business Challenge",
        priority="HOT",
        score=88,
        buyer_persona="Business Leader",
        business_fit="High",
        source_type="Public Business Discussion",
    )

    review_output = process_for_human_review(demo_signal)

    print(review_output)
