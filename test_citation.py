from app.utils.citation_formatter import (
    format_sources
)


def test_format_sources():

    documents = [
        {
            "source": "RDBMS-Unit2.pdf",
            "subject": "dbms",
            "content": "Normalization reduces redundancy.",
            "relevance": 85
        }
    ]

    sources = format_sources(
        documents
    )

    assert len(sources) == 1

    assert sources[0]["source"] == (
        "RDBMS-Unit2.pdf"
    )

    assert sources[0]["subject"] == "dbms"

    assert sources[0]["relevance"] == 85