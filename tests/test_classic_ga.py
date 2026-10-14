from core.classic_ga import run_classic_ga


def test_best_route_is_valid_permutation():
    result = run_classic_ga(n_cities=6, pop_size=10, n_generations=20, seed=1)
    assert sorted(result.best_route) == list(range(6))


def test_fitness_history_never_increases():
    # Elitizm garantisi: en iyi mesafe hiçbir nesilde artmamalı
    result = run_classic_ga(n_cities=6, pop_size=10, n_generations=30, seed=2)
    for i in range(1, len(result.fitness_history)):
        assert result.fitness_history[i] <= result.fitness_history[i - 1] + 1e-9


def test_result_fields_are_complete():
    result = run_classic_ga(n_cities=5, pop_size=8, n_generations=10, seed=0)
    assert len(result.cities) == 5
    assert len(result.cities[0]) == 2          # [x, y]
    assert len(result.fitness_history) == 10
    assert result.best_distance > 0


def test_different_seeds_give_different_results():
    r1 = run_classic_ga(n_cities=8, pop_size=10, n_generations=20, seed=1)
    r2 = run_classic_ga(n_cities=8, pop_size=10, n_generations=20, seed=99)
    assert r1.cities != r2.cities              # farklı şehir konumları


def test_same_seed_reproducible():
    r1 = run_classic_ga(n_cities=6, pop_size=10, n_generations=20, seed=42)
    r2 = run_classic_ga(n_cities=6, pop_size=10, n_generations=20, seed=42)
    assert r1.best_route == r2.best_route
    assert r1.best_distance == r2.best_distance
