import pytest
from unittest.mock import patch, MagicMock
import requests

from app.agentic.embeddings import (
    get_embedding_provider,
    HashedBagOfWordsEmbeddingProvider,
    SentenceTransformerEmbeddingProvider,
    OpenAIEmbeddingProvider
)
from app.agentic.llm_client import (
    get_llm_provider,
    MockPedagogicalLLMProvider,
    OpenAILLMProvider,
    GeminiLLMProvider,
    get_ai_diagnostics
)


def test_embedding_provider_selection():
    p_bow = get_embedding_provider("bag-of-words")
    assert isinstance(p_bow, HashedBagOfWordsEmbeddingProvider)
    assert p_bow.dimension == 384

    p_st = get_embedding_provider("sentence-transformers")
    assert isinstance(p_st, SentenceTransformerEmbeddingProvider)

    p_oa = get_embedding_provider("openai")
    assert isinstance(p_oa, OpenAIEmbeddingProvider)


def test_openai_embedding_provider_missing_key_fallback():
    provider = OpenAIEmbeddingProvider(api_key=None)
    vec = provider.embed_text("Test query text for embedding")
    assert len(vec) == 384
    # Ensure non-zero vector from fallback
    assert any(x != 0.0 for x in vec)


def test_openai_embedding_provider_api_error_fallback():
    provider = OpenAIEmbeddingProvider(api_key="sk-fake-key-for-test")
    with patch("requests.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_resp.text = "Unauthorized: Invalid API key"
        mock_post.return_value = mock_resp

        vec = provider.embed_text("Test query during API error")
        assert len(vec) == 384
        assert any(x != 0.0 for x in vec)


def test_llm_provider_selection():
    mock_llm = get_llm_provider("mock")
    assert isinstance(mock_llm, MockPedagogicalLLMProvider)
    assert mock_llm.provider_name == "mock:pedagogical-engine"

    oa_llm = get_llm_provider("openai")
    assert isinstance(oa_llm, OpenAILLMProvider)

    gemini_llm = get_llm_provider("gemini")
    assert isinstance(gemini_llm, GeminiLLMProvider)


def test_llm_unconfigured_api_key_graceful_fallback():
    oa_provider = OpenAILLMProvider(api_key=None)
    res = oa_provider.generate_tutor_response("system", "user prompt")
    assert res["is_fallback"] is True
    assert "fallback:mock-unconfigured-api-key" in res["provider_used"]
    assert res["text"] is None

    gemini_provider = GeminiLLMProvider(api_key=None)
    res_g = gemini_provider.generate_tutor_response("system", "user prompt")
    assert res_g["is_fallback"] is True
    assert "fallback:mock-unconfigured-api-key" in res_g["provider_used"]


def test_llm_timeout_handling_and_fallback():
    oa_provider = OpenAILLMProvider(api_key="sk-test-key")
    with patch("requests.post", side_effect=requests.exceptions.Timeout("Connection timed out")):
        res = oa_provider.generate_tutor_response("system", "user prompt", timeout_seconds=1.0)
        assert res["is_fallback"] is True
        assert res["provider_used"] == "fallback:mock-after-timeout"
        assert "timed out" in res["error_detail"]


def test_llm_malformed_and_error_response_handling():
    oa_provider = OpenAILLMProvider(api_key="sk-test-key")
    with patch("requests.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_resp.text = "Internal Server Error"
        mock_post.return_value = mock_resp

        res = oa_provider.generate_tutor_response("system", "user prompt")
        assert res["is_fallback"] is True
        assert res["provider_used"] == "fallback:mock-after-api-error"


def test_ai_diagnostics_no_secret_leakage():
    diag = get_ai_diagnostics()
    assert "status" in diag
    assert "llm_provider" in diag
    assert "embedding_provider" in diag
    assert "storage" in diag

    # Explicitly check that no secrets or API keys are present in string values
    diag_str = str(diag)
    assert "sk-" not in diag_str
    assert "password" not in diag_str.lower()
    assert "secret" not in diag_str.lower()
