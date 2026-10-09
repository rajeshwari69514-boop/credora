from app.services.conflict_service import (
    detect_source_conflict
)


def test_no_conflict_with_single_source():

    documents = [
        {
            "source": "source1.pdf",
            "content": "Database stores information."
        }
    ]

    result = detect_source_conflict(
        documents
    )

    assert result["conflict_detected"] is False