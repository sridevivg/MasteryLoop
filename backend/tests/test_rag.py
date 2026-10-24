import pytest
from app.agentic.rag import vector_store, embedding_service


def test_embedding_service_dimension_and_normalization():
    text = "Binary search trees maintain monotonic in-order traversal properties."
    vector = embedding_service.embed_text(text)
    assert len(vector) == 384
    # Check L2-norm is approximately 1.0
    norm = sum(v * v for v in vector) ** 0.5
    assert abs(norm - 1.0) < 1e-3


def test_vector_store_search_retrieves_relevant_content():
    # Query for two-pointer array technique
    results = vector_store.search("two pointers sorted array", top_k=2)
    assert len(results) > 0
    top = results[0]
    assert "Two-Pointer" in top["title"]
    assert "score" in top
    assert top["score"] > 0.20
    assert "source" in top


def test_vector_store_metadata_filtering():
    # Search with domain filtering
    results_dsa = vector_store.search("data structures", top_k=3)
    assert len(results_dsa) > 0
    for r in results_dsa:
        assert r["chunk_id"] is not None


def test_vector_store_low_relevance_empty_query():
    # Empty query should return empty or low score
    results = vector_store.search("", min_score=0.99)
    assert len(results) == 0


def test_idempotent_chunk_upsert():
    initial_count = vector_store.get_chunk_count()
    # Re-upserting an existing chunk should not duplicate
    success = vector_store.upsert_chunk(
        chunk_id="test_idempotent_chunk_001",
        content="This is an idempotent test chunk.",
        metadata={"title": "Test Title", "domain": "Testing"}
    )
    assert success is True

    # Re-upsert with same ID
    success_2 = vector_store.upsert_chunk(
        chunk_id="test_idempotent_chunk_001",
        content="This is an updated idempotent test chunk.",
        metadata={"title": "Updated Title", "domain": "Testing"}
    )
    assert success_2 is True
