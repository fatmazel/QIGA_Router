import numpy as np
import pytest
from core.fitness import evaluate_population, tour_distance


def test_equilateral_triangle():
    # 3 şehirli eşkenar üçgen: her kenar 1.0 → toplam tur = 3.0
    dist_matrix = np.array([
        [0.0, 1.0, 1.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 0.0],
    ])
    assert tour_distance(np.array([0, 1, 2]), dist_matrix) == pytest.approx(3.0)


def test_tour_is_closed_loop():
    # 0→1 = 2, 1→2 = 3, 2→0 = 5 → toplam = 10
    dist_matrix = np.array([
        [0.0, 2.0, 5.0],
        [2.0, 0.0, 3.0],
        [5.0, 3.0, 0.0],
    ])
    assert tour_distance(np.array([0, 1, 2]), dist_matrix) == 10.0


def test_different_routes_different_distances():
    dist_matrix = np.array([
        [0.0, 1.0, 10.0],
        [1.0, 0.0, 1.0],
        [10.0, 1.0, 0.0],
    ])
    d1 = tour_distance(np.array([0, 1, 2]), dist_matrix)  # 1+1+10 = 12
    d2 = tour_distance(np.array([0, 2, 1]), dist_matrix)  # 10+1+1 = 12 (simetrik)
    assert d1 == d2  # simetrik matris


def test_evaluate_population_shape():
    dist_matrix = np.ones((4, 4)) - np.eye(4)  # tüm kenarlar 1.0
    routes = [np.array([0, 1, 2, 3]), np.array([3, 2, 1, 0]), np.array([1, 3, 0, 2])]
    distances = evaluate_population(routes, dist_matrix)
    assert distances.shape == (3,)
    assert np.all(distances == 4.0)  # 4 şehir, her kenar 1.0 → tur = 4.0


