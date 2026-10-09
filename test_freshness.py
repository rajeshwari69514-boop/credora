from app.services.freshness_service import (
    check_source_freshness
)


def test_freshness_without_documents():

    result = check_source_freshness([])

    assert result["status"] == "Unavailable"

    assert result["sources"] == []