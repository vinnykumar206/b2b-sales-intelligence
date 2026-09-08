"""
B2B Sales Intelligence
Signal Ingestion & Deduplication Layer

This is a sanitized portfolio implementation demonstrating how
raw commercial signals can be normalized and deduplicated before
entering downstream intelligence processing.

Production-specific collectors, credentials, APIs, databases,
and private datasets are intentionally excluded.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Optional


@dataclass
class CommercialSignal:
    """
    Standardized representation of a business signal.

    The structure is intentionally generic so that signals from
    different public sources can enter the same processing pipeline.
    """

    signal_id: str
    source_type: str
    timestamp: datetime
    organization: Optional[str]
    author: Optional[str]
    content: str
    source_url: Optional[str] = None
    location: Optional[str] = None
    signal_type: Optional[str] = None


def normalize_text(text: str) -> str:
    """
    Normalize text for comparison and duplicate detection.

    The function removes unnecessary whitespace, normalizes case,
    and removes simple formatting noise.
    """

    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)

    return text.strip()


def generate_signal_fingerprint(signal: CommercialSignal) -> str:
    """
    Generate a stable fingerprint for a signal.

    The fingerprint uses normalized content together with source
    and organization context.

    This allows substantially identical signals to be detected
    without exposing or storing private production identifiers.
    """

    normalized_content = normalize_text(signal.content)

    fingerprint_input = "|".join(
        [
            normalize_text(signal.source_type),
            normalize_text(signal.organization or ""),
            normalized_content,
        ]
    )

    return hashlib.sha256(
        fingerprint_input.encode("utf-8")
    ).hexdigest()


def deduplicate_signals(
    signals: Iterable[CommercialSignal],
) -> list[CommercialSignal]:
    """
    Remove duplicate signals while preserving the first occurrence.

    Returns:
        A list containing unique signals.
    """

    unique_signals: list[CommercialSignal] = []
    fingerprints: set[str] = set()

    for signal in signals:
        fingerprint = generate_signal_fingerprint(signal)

        if fingerprint in fingerprints:
            continue

        fingerprints.add(fingerprint)
        unique_signals.append(signal)

    return unique_signals


def filter_recent_signals(
    signals: Iterable[CommercialSignal],
    reference_time: datetime,
    max_age_hours: int = 48,
) -> list[CommercialSignal]:
    """
    Keep signals inside the configured recency window.

    Recency is treated as an input to prioritization rather than
    proof that a signal is commercially valuable.
    """

    recent_signals: list[CommercialSignal] = []

    for signal in signals:
        age_hours = (
            reference_time - signal.timestamp
        ).total_seconds() / 3600

        if 0 <= age_hours <= max_age_hours:
            recent_signals.append(signal)

    return recent_signals


def prepare_signals(
    signals: Iterable[CommercialSignal],
    reference_time: datetime,
    max_age_hours: int = 48,
) -> list[CommercialSignal]:
    """
    Prepare raw signals for downstream intelligence processing.

    Processing order:

        1. Recency filtering
        2. Deduplication

    The function intentionally stops before intent classification,
    scoring, or commercial decision-making.
    """

    recent = filter_recent_signals(
        signals=signals,
        reference_time=reference_time,
        max_age_hours=max_age_hours,
    )

    return deduplicate_signals(recent)


if __name__ == "__main__":
    demo_time = datetime(2026, 9, 8, 12, 0, 0)

    demo_signals = [
        CommercialSignal(
            signal_id="SIG-DEMO-001",
            source_type="Public Business Discussion",
            timestamp=datetime(2026, 9, 8, 10, 30, 0),
            organization="Example Enterprise",
            author="Example Business Leader",
            content=(
                "We are evaluating ways to improve leadership capability "
                "as the organization scales."
            ),
            location="India",
        ),
        CommercialSignal(
            signal_id="SIG-DEMO-002",
            source_type="Public Business Discussion",
            timestamp=datetime(2026, 9, 8, 10, 35, 0),
            organization="Example Enterprise",
            author="Example Business Leader",
            content=(
                "We are evaluating ways to improve leadership capability "
                "as the organization scales."
            ),
            location="India",
        ),
    ]

    prepared = prepare_signals(
        signals=demo_signals,
        reference_time=demo_time,
    )

    print(f"Input signals: {len(demo_signals)}")
    print(f"Signals after processing: {len(prepared)}")

    for signal in prepared:
        print(
            f"- {signal.signal_id}: "
            f"{signal.organization} | "
            f"{signal.signal_type or 'Unclassified'}"
        )
