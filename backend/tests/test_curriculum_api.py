import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_domains():
    res = client.get("/api/v1/curriculum/domains")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 11
    domain_codes = {d["code"] for d in data}
    expected_codes = {
        "VERBAL", "QUANT", "REASONING", "PROG", "DSA",
        "SQL", "OOP", "DBMS", "OS", "NETWORKS", "ML"
    }
    assert expected_codes.issubset(domain_codes)
    for d in data:
        assert d["skill_count"] > 0
        assert d["topic_count"] > 0


def test_get_domain_hierarchy():
    res = client.get("/api/v1/curriculum/domains/DSA")
    assert res.status_code == 200
    data = res.json()
    assert data["code"] == "DSA"
    assert len(data["topics"]) > 0
    # verify subtopics and skills are nested
    first_topic = data["topics"][0]
    assert len(first_topic["subtopics"]) > 0
    first_subtopic = first_topic["subtopics"][0]
    assert len(first_subtopic["skills"]) > 0


def test_get_skill_details():
    res = client.get("/api/v1/curriculum/skills/DSA_BST")
    assert res.status_code == 200
    data = res.json()
    assert data["code"] == "DSA_BST"
    assert "Binary Search Trees" in data["name"]


def test_get_skill_prerequisites():
    # DSA_BST depends on DSA_BINARY_TREES, which depends on DSA_LINKED_LISTS, etc.
    res = client.get("/api/v1/curriculum/skills/DSA_BST/prerequisites")
    assert res.status_code == 200
    data = res.json()
    assert data["target_skill"]["code"] == "DSA_BST"
    
    # Direct prerequisites should include binary trees
    direct_codes = {p["code"] for p in data["direct_prerequisites"]}
    assert "DSA_BINARY_TREES" in direct_codes

    # Foundational prerequisites should include linked lists
    foundational_codes = {p["code"] for p in data["foundational_prerequisites_topological"]}
    assert "DSA_LINKED_LISTS" in foundational_codes


def test_get_skill_graph():
    res = client.get("/api/v1/curriculum/graph")
    assert res.status_code == 200
    data = res.json()
    assert len(data["nodes"]) >= 50
    assert len(data["edges"]) >= 40
    # verify node structure
    first_node = data["nodes"][0]
    assert "id" in first_node
    assert "label" in first_node
    assert "domain" in first_node


def test_validate_curriculum_dag():
    res = client.get("/api/v1/curriculum/validate-dag")
    assert res.status_code == 200
    data = res.json()
    assert data["is_valid_dag"] is True
    assert data["total_skills"] >= 50
    assert data["total_prerequisite_edges"] >= 40
    assert data["topological_sequence_count"] >= 50
