import numpy as np
import pytest
from core.chromosome import QuantumChromosome


def test_initial_theta_is_pi_over_4():
    # Başlangıç açısı tam süperpozisyon: π/4
    rng = np.random.default_rng(0)
    chrom = QuantumChromosome(5, rng)
    assert np.allclose(chrom.theta, np.pi / 4)


def test_observe_is_valid_permutation():
    rng = np.random.default_rng(0)
    chrom = QuantumChromosome(6, rng)
    route = chrom.observe(rng)
    assert route.shape == (6,)
    assert sorted(route.tolist()) == list(range(6))


def test_observe_different_each_call():
    # Gürültü sayesinde her gözlem farklı rota üretmeli
    rng = np.random.default_rng(99)
    chrom = QuantumChromosome(8, rng)
    routes = [chrom.observe(rng).tolist() for _ in range(10)]
    assert len(set(tuple(r) for r in routes)) > 1


def test_rotate_changes_theta():
    rng = np.random.default_rng(0)
    chrom = QuantumChromosome(5, rng)
    theta_before = chrom.theta.copy()
    best_route = np.array([2, 0, 4, 1, 3])
    chrom.rotate(best_route, delta=0.05)
    assert not np.allclose(chrom.theta, theta_before)


def test_theta_stays_in_valid_range_after_many_rotations():
    # Aşırı rotasyondan sonra bile [0, π/2] sınırı korunmalı
    rng = np.random.default_rng(7)
    chrom = QuantumChromosome(5, rng)
    best_route = np.array([4, 3, 2, 1, 0])
    for _ in range(200):
        chrom.rotate(best_route, delta=0.1)
    assert np.all(chrom.theta >= 0.0)
    assert np.all(chrom.theta <= np.pi / 2)
