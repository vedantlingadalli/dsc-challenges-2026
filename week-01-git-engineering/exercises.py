
"""Week 0: Python Fundamentals Bootcamp — Beginner Practice Tasks."""

import csv
import json
from typing import Dict, List, Tuple, Any


def evaluate_attendance_status(attended: int, total: int) -> str:
    """Return 'ELIGIBLE' (>=75%), 'WARNING' (65% to <75%), or 'SHORTAGE' (<65%).

    If total <= 0, return 'NO_SESSIONS'.
    """
    if total <= 0:
        return "NO_SESSIONS"
    percentage = (attended / total) * 100
    if percentage >= 75:
        return "ELIGIBLE"
    elif percentage >= 65:
        return "WARNING"
    else:
        return "SHORTAGE"


def safe_parse_float(raw_value: Any, default: float = 0.0) -> float:
    """Convert raw_value to float safely using try/except. Return default on failure."""
    try:
        if raw_value is None or isinstance(raw_value, bool):
            return default
        return float(raw_value)
    except (ValueError, TypeError):
        return default


def analyze_pod_scores(records: List[Tuple[str, str, float]]) -> Dict[str, Any]:
    """Analyze (usn, pod_name, score) tuples using sets, dicts, and comprehensions.

    Returns a dictionary with keys:
        - 'unique_student_count': int (number of unique USNs via set)
        - 'high_scorers': List[str] (USNs with score >= 80 using a list comprehension)
        - 'pod_averages': Dict[str, float] (average score per pod rounded to 2 decimals)
    """
    unique_usns = {usn for usn, _, _ in records}
    high_scorers = [usn for usn, _, score in records if score >= 80]

    pod_totals: Dict[str, List[float]] = {}
    for _, pod_name, score in records:
        pod_totals.setdefault(pod_name, []).append(score)

    pod_averages = {
        pod: round(sum(scores) / len(scores), 2)
        for pod, scores in pod_totals.items()
    }

    return {
        "unique_student_count": len(unique_usns),
        "high_scorers": high_scorers,
        "pod_averages": pod_averages,
    }


def summarize_csv_to_json(csv_path: str, json_path: str) -> Dict[str, Any]:
    """Read cohort CSV using built-in csv module and export summary JSON.

    Summary dictionary must contain:
        - 'total_students': int
        - 'branches': List[str] (sorted unique branch codes)
        - 'average_score': float (rounded to 2 decimals)
    """
    rows = []
    with open(csv_path, mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    total_students = len(rows)
    branches = sorted({row["branch"].strip() for row in rows if row.get("branch")})
    scores = [float(row["score"]) for row in rows if row.get("score") not in (None, "")]
    average_score = round(sum(scores) / len(scores), 2) if scores else 0.0

    summary = {
        "total_students": total_students,
        "branches": branches,
        "average_score": average_score,
    }

    with open(json_path, mode="w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


class StudentRecord:
    """Tracks weekly evaluation scores for a single DSC recruit."""

    def __init__(self, usn: str, name: str):
        """Initialize record with uppercase USN, name, and empty scores list."""
        self.usn = usn.upper()
        self.name = name
        self.scores: List[float] = []

    def add_score(self, score: float) -> None:
        """Append a score (must be between 0 and 100; raise ValueError otherwise)."""
        if not (0 <= score <= 100):
            raise ValueError(f"Score must be between 0 and 100, got {score}")
        self.scores.append(float(score))

    def average(self) -> float:
        """Return average score rounded to 2 decimals, or 0.0 if no scores exist."""
        if not self.scores:
            return 0.0
        return round(sum(self.scores) / len(self.scores), 2)

    def is_passing(self, threshold: float = 50.0) -> bool:
        """Return True if average() >= threshold, else False."""
        return self.average() >= threshold
