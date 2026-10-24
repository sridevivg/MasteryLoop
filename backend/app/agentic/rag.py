"""
Curriculum Vector Store and Semantic Retrieval Engine for MasteryLoop.
Integrates with Qdrant for dense vector search with metadata filtering,
deterministic embedding generation fallback, and citation attribution.
"""

import re
import math
import logging
import hashlib
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from qdrant_client.http.exceptions import UnexpectedResponse

from app.core.config import settings
from app.agentic.embeddings import (
    get_embedding_provider,
    BaseEmbeddingProvider,
    HashedBagOfWordsEmbeddingProvider,
    DEFAULT_VECTOR_DIMENSION
)

logger = logging.getLogger(__name__)

VECTOR_DIMENSION = DEFAULT_VECTOR_DIMENSION
COLLECTION_NAME = "masteryloop_curriculum"

# Default singleton provider
embedding_service = get_embedding_provider()


class CurriculumVectorStore:
    """Manages Qdrant vector collection for curriculum knowledge grounding."""

    def __init__(self, url: Optional[str] = None, path: Optional[str] = None, provider: Optional[BaseEmbeddingProvider] = None):
        self.url = url or settings.QDRANT_URL
        self.path = path or settings.QDRANT_PATH
        self.embedding_provider = provider or get_embedding_provider()

        if self.path:
            try:
                self.client = QdrantClient(path=self.path)
                logger.info(f"Initialized persistent local on-disk Qdrant at: {self.path}")
            except Exception as e:
                logger.warning(f"Could not initialize local Qdrant at {self.path}: {e}. Falling back to in-memory.")
                self.client = QdrantClient(":memory:")
        elif not self.url or self.url == ":memory:":
            self.client = QdrantClient(":memory:")
            logger.info("Initialized in-memory Qdrant instance for curriculum RAG.")
        else:
            try:
                self.client = QdrantClient(url=self.url, api_key=settings.QDRANT_API_KEY)
                logger.info(f"Connected to remote Qdrant at {self.url}")
            except Exception as e:
                logger.warning(f"Could not connect to Qdrant at {self.url}: {e}. Falling back to in-memory store.")
                self.client = QdrantClient(":memory:")

        self._ensure_collection()

    def get_diagnostics(self) -> Dict[str, Any]:
        """Provides safe diagnostic metadata about vector store without credentials."""
        backend_type = "persistent-disk" if self.path else ("in-memory" if self.url == ":memory:" else "remote")
        return {
            "collection_name": COLLECTION_NAME,
            "vector_dimension": self.embedding_provider.dimension,
            "embedding_provider": self.embedding_provider.provider_name,
            "indexed_chunks": self.get_chunk_count(),
            "storage_backend": backend_type
        }

    def _ensure_collection(self):
        """Creates the curriculum collection in Qdrant if it does not exist, or validates dimension."""
        try:
            collections = self.client.get_collections().collections
            names = [c.name for c in collections]
            target_dim = self.embedding_provider.dimension

            if COLLECTION_NAME not in names:
                self.client.create_collection(
                    collection_name=COLLECTION_NAME,
                    vectors_config=qmodels.VectorParams(
                        size=target_dim,
                        distance=qmodels.Distance.COSINE
                    )
                )
                logger.info(f"Created Qdrant collection: {COLLECTION_NAME} (dimension={target_dim})")
            else:
                # Dimension verification safeguard
                try:
                    info = self.client.get_collection(COLLECTION_NAME)
                    existing_dim = info.config.params.vectors.size
                    if existing_dim != target_dim:
                        logger.warning(
                            f"Qdrant collection dimension mismatch! Existing: {existing_dim}, "
                            f"Current Provider: {target_dim}. Recreating collection to prevent vector errors."
                        )
                        self.client.delete_collection(COLLECTION_NAME)
                        self.client.create_collection(
                            collection_name=COLLECTION_NAME,
                            vectors_config=qmodels.VectorParams(
                                size=target_dim,
                                distance=qmodels.Distance.COSINE
                            )
                        )
                except Exception as check_err:
                    logger.debug(f"Collection dimension check notice: {check_err}")
        except Exception as e:
            logger.error(f"Error initializing Qdrant collection: {e}")

    def upsert_chunk(
        self,
        chunk_id: str,
        content: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """
        Idempotently inserts or updates a curriculum chunk with metadata.
        Uses deterministic point ID derived from chunk_id string.
        """
        try:
            full_text = f"{metadata.get('title', '')} {metadata.get('topic', '')} {metadata.get('domain', '')} {content}".strip()
            vector = self.embedding_provider.embed_text(full_text)
            # Create integer or UUID point ID
            point_id = int(hashlib.md5(chunk_id.encode("utf-8")).hexdigest()[:15], 16)

            payload = {
                "chunk_id": chunk_id,
                "content": content,
                **metadata
            }

            self.client.upsert(
                collection_name=COLLECTION_NAME,
                points=[
                    qmodels.PointStruct(
                        id=point_id,
                        vector=vector,
                        payload=payload
                    )
                ]
            )
            return True
        except Exception as e:
            logger.error(f"Failed to upsert chunk {chunk_id}: {e}")
            return False

    def search(
        self,
        query: str,
        skill_id: Optional[str] = None,
        domain_name: Optional[str] = None,
        top_k: int = 4,
        min_score: float = 0.20
    ) -> List[Dict[str, Any]]:
        """
        Retrieves top-k curriculum chunks matching the query with optional skill/domain filtering.
        """
        try:
            query_vector = self.embedding_provider.embed_text(query)

            # Build metadata filters if specified
            filter_conditions = []
            if skill_id:
                filter_conditions.append(
                    qmodels.FieldCondition(
                        key="skill_id",
                        match=qmodels.MatchValue(value=skill_id)
                    )
                )
            if domain_name:
                filter_conditions.append(
                    qmodels.FieldCondition(
                        key="domain",
                        match=qmodels.MatchValue(value=domain_name)
                    )
                )

            q_filter = qmodels.Filter(must=filter_conditions) if filter_conditions else None

            # Qdrant search - support both query_points (modern >=1.10) and search
            if hasattr(self.client, "query_points"):
                response = self.client.query_points(
                    collection_name=COLLECTION_NAME,
                    query=query_vector,
                    query_filter=q_filter,
                    limit=top_k
                )
                search_results = response.points
            else:
                search_results = self.client.search(
                    collection_name=COLLECTION_NAME,
                    query_vector=query_vector,
                    query_filter=q_filter,
                    limit=top_k
                )

            results = []
            for hit in search_results:
                score = round(float(hit.score), 4)
                if score >= min_score:
                    results.append({
                        "chunk_id": hit.payload.get("chunk_id"),
                        "title": hit.payload.get("title", "Curriculum Topic"),
                        "content": hit.payload.get("content", ""),
                        "skill_id": hit.payload.get("skill_id"),
                        "domain": hit.payload.get("domain"),
                        "topic": hit.payload.get("topic"),
                        "content_type": hit.payload.get("content_type", "CONCEPT"),
                        "score": score,
                        "source": hit.payload.get("source", "MasteryLoop Verified Curriculum")
                    })

            return results
        except Exception as e:
            logger.error(f"Search query error: {e}")
            return []

    def get_chunk_count(self) -> int:
        """Returns the total number of indexed points."""
        try:
            res = self.client.get_collection(COLLECTION_NAME)
            return res.points_count or 0
        except Exception:
            return 0


# Global singleton instance
vector_store = CurriculumVectorStore()
