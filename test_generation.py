from app.services.generation_service import generate_answer


def test_generation_with_context(monkeypatch):

    class FakeResponse:
        text = "Normalization reduces data redundancy."

    def fake_generate_content(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        "app.services.generation_service.gemini_client.models.generate_content",
        fake_generate_content
    )

    result = generate_answer(
        "What is normalization?",
        "Normalization reduces data redundancy."
    )

    assert "answer" in result
    assert result["provider"] == "Gemini"