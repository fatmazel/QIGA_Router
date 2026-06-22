import numpy as np
from core.distance import generate_cities, compute_distance_matrix


def test_generate_cities_shape():
    coords = generate_cities(n=10, seed=0)
    assert coords.shape == (10, 2)


def test_generate_cities_range():
    coords = generate_cities(n=100, seed=1)
    assert coords.min() >= 0.0
    assert coords.max() <= 100.0


def test_distance_matrix_shape():
    coords = generate_cities(n=5, seed=0)
    D = compute_distance_matrix(coords)
    assert D.shape == (5, 5)


def test_distance_matrix_diagonal_zero():
    coords = generate_cities(n=5, seed=0)
    D = compute_distance_matrix(coords)
    np.testing.assert_array_almost_equal(np.diag(D), 0.0)


def test_distance_matrix_symmetric():
    coords = generate_cities(n=5, seed=0)
    D = compute_distance_matrix(coords)
    np.testing.assert_array_almost_equal(D, D.T)


def test_known_distance():
    # (0,0) ve (3,4) arası mesafe = 5 (3-4-5 üçgeni)
    coords = np.array([[0.0, 0.0], [3.0, 4.0]])
    D = compute_distance_matrix(coords)
    assert abs(D[0][1] - 5.0) < 1e-9
