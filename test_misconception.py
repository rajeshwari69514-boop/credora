from app.services import misconception_service


def test_misconception_detection(monkeypatch):

    class FakeResponse:
        text = (
            "MISCONCEPTION: No\n"
            "EXPLANATION: The question is valid.\n"
            "CORRECTION: Not needed"
        )

    def fake_generate_content(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        misconception_service.gemini_client.models,
        "generate_content",
        fake_generate_content
    )

    result = misconception_service.detect_misconception(
        "What is normalization?",
        "Normalization reduces data redundancy."
    )

    assert "MISCONCEPTION: No" in result
    assert "EXPLANATION:" in result
    assert "CORRECTION:" in result