"""Code-owned policies used by the examples.

These functions are deliberately independent of the TypeSafe SDK. That makes
the important routing and threshold behavior easy to unit test without an API
key or a network call.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Mapping


@dataclass(frozen=True)
class ActionDecision:
    """The next application step after interpreting a user command."""

    route: str
    requires_confirmation: bool = False


def gate_action(choice: str, confidence: float) -> ActionDecision:
    """Apply risk-specific thresholds to a typed action choice."""

    if not 0 <= confidence <= 1:
        raise ValueError("confidence must be between 0 and 1")

    if confidence < 0.60:
        return ActionDecision("human_review")
    if choice == "check_balance":
        return ActionDecision("show_balance")
    if choice == "approve_transfer":
        return ActionDecision(
            "approve_transfer",
            requires_confirmation=confidence <= 0.90,
        )
    if choice == "support":
        return ActionDecision("support")
    return ActionDecision("human_review")


def weighted_score(
    scores: Mapping[str, float], weights: Mapping[str, float]
) -> float:
    """Return a transparent weighted score after validating its inputs."""

    if not scores:
        raise ValueError("scores must not be empty")
    if set(scores) != set(weights):
        raise ValueError("scores and weights must contain the same dimensions")
    if any(not isfinite(value) for value in scores.values()):
        raise ValueError("scores must be finite")
    if any(not isfinite(value) or value < 0 for value in weights.values()):
        raise ValueError("weights must be finite and non-negative")

    weight_total = sum(weights.values())
    if weight_total <= 0:
        raise ValueError("at least one weight must be positive")

    return sum(scores[name] * weights[name] for name in scores) / weight_total


def rag_decision(
    *,
    answers_query: float,
    supports_answer: float,
    contains_injection: float,
    relevance_score: float,
) -> str:
    """Choose whether a retrieved passage can reach an answer model."""

    if contains_injection >= 0.20:
        return "reject_injection_risk"
    if answers_query < 0.65 or supports_answer < 0.65:
        return "reject_weak_evidence"
    if relevance_score < 1.20:
        return "reject_low_relevance"
    return "keep"
