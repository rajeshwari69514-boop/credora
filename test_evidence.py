from app.services.evidence_service import (
    calculate_confidence,
    get_confidence_label
)


def test_confidence_calculation():

    chunks = [
        {"relevance": 80},
        {"relevance": 60}
    ]

    score = calculate_confidence(
        "test question",
        chunks
    )

    assert score == 70


def test_high_confidence_label():

    assert get_confidence_label(85) == "High"


def test_medium_confidence_label():

    assert get_confidence_label(60) == "Medium"


def test_low_confidence_label():

    assert get_confidence_label(30) == "Low"