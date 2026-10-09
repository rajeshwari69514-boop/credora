from app.services.retrieval_service import detect_subject


def test_detect_dbms_subject():

    subjects = detect_subject(
        "What is normalization in DBMS?"
    )

    assert "dbms" in subjects


def test_detect_programming_subject():

    subjects = detect_subject(
        "What is a Python function?"
    )

    assert "programming" in subjects


def test_detect_maths_subject():

    subjects = detect_subject(
        "Explain probability"
    )

    assert "maths" in subjects