from core.benchmark import run_benchmark


def test_run_benchmark_returns_expected_structure():
    results = run_benchmark(n_cities_list=[5, 8], pop_size=8, n_generations=10, seed=1)
    assert len(results) == 2

    for row, expected_n in zip(results, [5, 8]):
        assert row["n_cities"] == expected_n
        assert row["qiga_distance"] > 0
        assert row["ga_distance"] > 0
        assert row["qiga_time"] >= 0
        assert row["ga_time"] >= 0


def test_run_benchmark_same_seed_is_reproducible():
    r1 = run_benchmark(n_cities_list=[6], pop_size=8, n_generations=10, seed=7)
    r2 = run_benchmark(n_cities_list=[6], pop_size=8, n_generations=10, seed=7)
    assert r1[0]["qiga_distance"] == r2[0]["qiga_distance"]
    assert r1[0]["ga_distance"] == r2[0]["ga_distance"]
