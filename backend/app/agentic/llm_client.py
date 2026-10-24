"""
Configurable LLM Provider Client for MasteryLoop Socratic AI Tutor.
Supports:
1. Mock Pedagogical Provider (deterministic, offline, rule-grounded development engine)
2. OpenAI Provider (gpt-4o-mini or configured model via REST API)
3. Google Gemini Provider (gemini-1.5-flash via REST API)

Provides graceful fallback, timeout protection, and safe diagnostic reporting.
"""

import logging
import requests
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from app.core.config import settings

logger = logging.getLogger(__name__)


class BaseLLMProvider(ABC):
    """Abstract base class for Socratic LLM inference providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Returns the canonical provider identifier."""
        pass

    @abstractmethod
    def generate_tutor_response(
        self,
        system_prompt: str,
        user_prompt: str,
        timeout_seconds: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Executes text completion with fallback handling.
        Returns dict with keys:
          - text: Optional[str] (None indicates caller should use pedagogical fallback)
          - provider_used: str
          - is_fallback: bool
          - error_detail: Optional[str]
        """
        pass


class MockPedagogicalLLMProvider(BaseLLMProvider):
    """
    Deterministic rule-based pedagogical engine.
    Produces high-fidelity, Bloom-aligned, multilingual responses without network latency.
    """

    @property
    def provider_name(self) -> str:
        return "mock:pedagogical-engine"

    def generate_tutor_response(
        self,
        system_prompt: str,
        user_prompt: str,
        timeout_seconds: Optional[float] = None
    ) -> Dict[str, Any]:
        return {
            "text": None,  # Signals tutor.py to format using its tested pedagogical template
            "provider_used": self.provider_name,
            "is_fallback": False,
            "error_detail": None
        }


class OpenAILLMProvider(BaseLLMProvider):
    """
    OpenAI Chat Completion provider (gpt-4o-mini or configured model).
    Enforces strict timeouts and catches API/network errors gracefully.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.OPENAI_MODEL

    @property
    def provider_name(self) -> str:
        return f"openai:{self.model}"

    def generate_tutor_response(
        self,
        system_prompt: str,
        user_prompt: str,
        timeout_seconds: Optional[float] = None
    ) -> Dict[str, Any]:
        timeout = timeout_seconds or settings.LLM_TIMEOUT_SECONDS

        if not self.api_key:
            logger.info("OpenAI API key not configured. Falling back to MockPedagogicalLLMProvider.")
            return {
                "text": None,
                "provider_used": "fallback:mock-unconfigured-api-key",
                "is_fallback": True,
                "error_detail": "OPENAI_API_KEY is not set in environment."
            }

        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            body = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.4,
                "max_tokens": 800
            }

            res = requests.post(url, json=body, headers=headers, timeout=timeout)
            if res.status_code == 200:
                data = res.json()
                content = data["choices"][0]["message"]["content"]
                return {
                    "text": content,
                    "provider_used": self.provider_name,
                    "is_fallback": False,
                    "error_detail": None
                }
            else:
                logger.warning(f"OpenAI API error HTTP {res.status_code}: {res.text}")
                return {
                    "text": None,
                    "provider_used": "fallback:mock-after-api-error",
                    "is_fallback": True,
                    "error_detail": f"HTTP {res.status_code}: {res.text[:100]}"
                }
        except requests.exceptions.Timeout:
            logger.warning(f"OpenAI request timed out after {timeout}s. Falling back to local engine.")
            return {
                "text": None,
                "provider_used": "fallback:mock-after-timeout",
                "is_fallback": True,
                "error_detail": f"Request timed out after {timeout}s."
            }
        except Exception as e:
            logger.warning(f"OpenAI request failed: {e}. Falling back to local engine.")
            return {
                "text": None,
                "provider_used": "fallback:mock-after-exception",
                "is_fallback": True,
                "error_detail": str(e)
            }


class GeminiLLMProvider(BaseLLMProvider):
    """
    Google Gemini inference provider (gemini-1.5-flash or configured model).
    Calls Google GenAI REST API with timeout protection and fallbacks.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model = model or settings.GEMINI_MODEL

    @property
    def provider_name(self) -> str:
        return f"gemini:{self.model}"

    def generate_tutor_response(
        self,
        system_prompt: str,
        user_prompt: str,
        timeout_seconds: Optional[float] = None
    ) -> Dict[str, Any]:
        timeout = timeout_seconds or settings.LLM_TIMEOUT_SECONDS

        if not self.api_key:
            logger.info("Gemini API key not configured. Falling back to MockPedagogicalLLMProvider.")
            return {
                "text": None,
                "provider_used": "fallback:mock-unconfigured-api-key",
                "is_fallback": True,
                "error_detail": "GEMINI_API_KEY is not set in environment."
            }

        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
            body = {
                "system_instruction": {
                    "parts": [{"text": system_prompt}]
                },
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": user_prompt}]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.4,
                    "maxOutputTokens": 800
                }
            }
            res = requests.post(url, json=body, timeout=timeout)
            if res.status_code == 200:
                data = res.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "text": text,
                    "provider_used": self.provider_name,
                    "is_fallback": False,
                    "error_detail": None
                }
            else:
                logger.warning(f"Gemini API error HTTP {res.status_code}: {res.text}")
                return {
                    "text": None,
                    "provider_used": "fallback:mock-after-api-error",
                    "is_fallback": True,
                    "error_detail": f"HTTP {res.status_code}: {res.text[:100]}"
                }
        except requests.exceptions.Timeout:
            logger.warning(f"Gemini request timed out after {timeout}s. Falling back to local engine.")
            return {
                "text": None,
                "provider_used": "fallback:mock-after-timeout",
                "is_fallback": True,
                "error_detail": f"Request timed out after {timeout}s."
            }
        except Exception as e:
            logger.warning(f"Gemini request failed: {e}. Falling back to local engine.")
            return {
                "text": None,
                "provider_used": "fallback:mock-after-exception",
                "is_fallback": True,
                "error_detail": str(e)
            }


def get_llm_provider(provider_type: Optional[str] = None) -> BaseLLMProvider:
    """Factory to retrieve configured LLM provider."""
    chosen = (provider_type or settings.LLM_PROVIDER).lower().strip()
    if chosen == "openai":
        return OpenAILLMProvider()
    elif chosen in ("gemini", "google"):
        return GeminiLLMProvider()
    else:
        return MockPedagogicalLLMProvider()


def get_ai_diagnostics() -> Dict[str, Any]:
    """Safe diagnostic report of active AI providers without leaking secrets."""
    from app.agentic.rag import vector_store

    active_llm = get_llm_provider()
    vec_diag = vector_store.get_diagnostics()

    return {
        "status": "operational",
        "llm_provider": {
            "active_provider": active_llm.provider_name,
            "configured_type": settings.LLM_PROVIDER,
            "openai_configured": bool(settings.OPENAI_API_KEY),
            "gemini_configured": bool(settings.GEMINI_API_KEY),
            "timeout_seconds": settings.LLM_TIMEOUT_SECONDS
        },
        "embedding_provider": {
            "active_provider": vec_diag["embedding_provider"],
            "configured_type": settings.EMBEDDING_PROVIDER,
            "dimension": vec_diag["vector_dimension"],
            "indexed_chunks": vec_diag["indexed_chunks"]
        },
        "storage": {
            "qdrant_backend": vec_diag["storage_backend"],
            "collection": vec_diag["collection_name"]
        }
    }
