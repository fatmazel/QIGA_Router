"""
FastAPI endpoint testleri — httpx.AsyncClient ile senkron pytest içinde çalışır.
"""

import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_solve_default_params():
    resp = client.post("/api/v1/solve", json={})
    assert resp.status_code == 200
    body = resp.json()
    assert "best_route" in body
    assert "best_distance" in body
    assert "fitness_history" in body
    assert "cities" in body


def test_solve_route_is_valid_permutation():
    resp = client.post("/api/v1/solve", json={"n_cities": 8, "n_generations": 20})
    body = resp.json()
    assert sorted(body["best_route"]) == list(range(8))


def test_solve_fitness_history_length():
    n_gen = 15
    resp = client.post("/api/v1/solve", json={"n_generations": n_gen, "n_cities": 5})
    body = resp.json()
    assert len(body["fitness_history"]) == n_gen


def test_cities_endpoint():
    resp = client.post("/api/v1/cities", json={"n": 5, "seed": 1})
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["cities"]) == 5
    assert len(body["distance_matrix"]) == 5
    assert len(body["distance_matrix"][0]) == 5


def test_solve_invalid_n_cities():
    # n_cities < 4 → validation error
    resp = client.post("/api/v1/solve", json={"n_cities": 2})
    assert resp.status_code == 422
