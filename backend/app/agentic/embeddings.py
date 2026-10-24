"""
Multilingual Embedding Provider Abstraction for MasteryLoop.
Supports:
1. Hashed Bag-of-Words (deterministic, fast, zero-dependency offline/development mode)
2. SentenceTransformers (pretrained multilingual e.g. paraphrase-multilingual-MiniLM-L12-v2)
3. OpenAI Embeddings (text-embedding-3-small with 384-D projection)

Provides graceful fallbacks and observable diagnostic metadata.
"""

import re
import math
import logging
import hashlib
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import requests

from app.core.config import settings

logger = logging.getLogger(__name__)

DEFAULT_VECTOR_DIMENSION = 384


class BaseEmbeddingProvider(ABC):
    """Abstract base class for all semantic embedding providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Returns the canonical provider identifier."""
        pass

    @property
    def dimension(self) -> int:
        """Embedding vector dimension."""
        return DEFAULT_VECTOR_DIMENSION

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Embeds a single string into a normalized dense vector."""
        pass

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Batch embedding with fallback loop."""
        return [self.embed_text(t) for t in texts]


class HashedBagOfWordsEmbeddingProvider(BaseEmbeddingProvider):
    """
    Deterministic semantic n-gram bag-of-words projection.
    Provides offline, zero-network, reproducible embeddings with plural normalization
    and bigram feature expansion.
    """

    @property
    def provider_name(self) -> str:
        return "bag-of-words"

    def embed_text(self, text: str) -> List[float]:
        if not text:
            return [0.0] * self.dimension

        # Tokenize words supporting English, Tamil, and other Unicode scripts
        words = re.findall(r'[\w]+', text.lower())
        vector = [0.0] * self.dimension

        for i, word in enumerate(words):
            stem = word[:-1] if len(word) > 3 and word.endswith('s') else word
            weight = math.log1p(len(stem))
            h = int(hashlib.sha256(stem.encode("utf-8")).hexdigest(), 16)
            idx = h % self.dimension
            sign = 1.0 if ((h >> 8) & 1) else -1.0
            vector[idx] += sign * weight

            if i > 0:
                prev_stem = words[i-1][:-1] if len(words[i-1]) > 3 and words[i-1].endswith('s') else words[i-1]
                bigram = f"{prev_stem}_{stem}"
                bh = int(hashlib.sha256(bigram.encode("utf-8")).hexdigest(), 16)
                bidx = bh % self.dimension
                bsign = 1.0 if ((bh >> 8) & 1) else -1.0
                vector[bidx] += bsign * (weight * 1.5)

        norm = math.sqrt(sum(v * v for v in vector))
        if norm > 1e-9:
            vector = [v / norm for v in vector]
        return vector


class SentenceTransformerEmbeddingProvider(BaseEmbeddingProvider):
    """
    Local pretrained multilingual transformer model (e.g. paraphrase-multilingual-MiniLM-L12-v2).
    Supports English, Tamil, and 50+ languages natively.
    """

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL_NAME
        self._model = None
        self._fallback = HashedBagOfWordsEmbeddingProvider()

    @property
    def provider_name(self) -> str:
        return f"sentence-transformers:{self.model_name}"

    def _load_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                logger.info(f"Loading SentenceTransformer model: {self.model_name}")
                self._model = SentenceTransformer(self.model_name)
            except Exception as e:
                logger.warning(
                    f"Could not load SentenceTransformer ({self.model_name}): {e}. "
                    "Falling back to HashedBagOfWordsEmbeddingProvider."
                )
                self._model = False

    def embed_text(self, text: str) -> List[float]:
        self._load_model()
        if self._model:
            try:
                vec = self._model.encode(text, normalize_embeddings=True)
                return [float(x) for x in vec[:self.dimension]]
            except Exception as e:
                logger.error(f"Error generating embedding with SentenceTransformer: {e}")
                return self._fallback.embed_text(text)
        return self._fallback.embed_text(text)


class OpenAIEmbeddingProvider(BaseEmbeddingProvider):
    """
    OpenAI dense embedding provider (text-embedding-3-small).
    Projects to 384 dimensions matching collection configuration.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self._fallback = HashedBagOfWordsEmbeddingProvider()

    @property
    def provider_name(self) -> str:
        return "openai:text-embedding-3-small"

    def embed_text(self, text: str) -> List[float]:
        if not self.api_key:
            logger.warning("OpenAI API key missing. Falling back to Bag-of-Words provider.")
            return self._fallback.embed_text(text)

        try:
            url = "https://api.openai.com/v1/embeddings"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            body = {
                "input": text,
                "model": "text-embedding-3-small",
                "dimensions": self.dimension
            }
            res = requests.post(url, json=body, headers=headers, timeout=5.0)
            if res.status_code == 200:
                data = res.json()
                vec = data["data"][0]["embedding"]
                # Ensure L2 normalized
                norm = math.sqrt(sum(v * v for v in vec))
                return [v / norm for v in vec] if norm > 1e-9 else vec
            else:
                logger.error(f"OpenAI embedding API returned status {res.status_code}: {res.text}")
                return self._fallback.embed_text(text)
        except Exception as e:
            logger.error(f"OpenAI embedding request failed: {e}. Using fallback.")
            return self._fallback.embed_text(text)


def get_embedding_provider(provider_type: Optional[str] = None) -> BaseEmbeddingProvider:
    """Factory to retrieve configured embedding provider with reliable fallbacks."""
    chosen = (provider_type or settings.EMBEDDING_PROVIDER).lower().strip()
    if chosen in ("st", "sentence-transformers", "sentence_transformers"):
        return SentenceTransformerEmbeddingProvider()
    elif chosen in ("openai", "openai-embeddings"):
        return OpenAIEmbeddingProvider()
    else:
        return HashedBagOfWordsEmbeddingProvider()
