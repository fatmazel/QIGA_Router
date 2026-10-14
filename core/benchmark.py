"""
QIGA vs Klasik GA karşılaştırma betiği.

Her n_cities değeri için iki algoritma aynı şehir koordinatlarıyla (aynı seed)
çalıştırılır; en iyi tur mesafesi ve çalışma süresi ölçülüp tablo halinde
terminale yazdırılır.

Çalıştırmak için (proje kökünden):
  python -m core.benchmark
"""

from __future__ import annotations

import time

import matplotlib

matplotlib.use("Agg")  # Ekran olmadan (headless) PNG üretimi için
import matplotlib.pyplot as plt

from core.classic_ga import run_classic_ga
from core.qiga import run_qiga

DEFAULT_N_CITIES = [10, 20, 30, 50]
DEFAULT_POP_SIZE = 30
DEFAULT_N_GENERATIONS = 150
DEFAULT_SEED = 42
DEFAULT_PLOT_PATH = "docs/benchmark.png"

# Kategorik renk sırası sabit tutulur: QIGA mavi, GA turuncu
_COLOR_QIGA = "#2a78d6"
_COLOR_GA = "#eb6834"
_COLOR_GRID = "#e1e0d9"
_COLOR_INK = "#0b0b0b"
_COLOR_MUTED = "#898781"
_COLOR_SURFACE = "#fcfcfb"


def run_benchmark(
    n_cities_list: list[int] = DEFAULT_N_CITIES,
    pop_size: int = DEFAULT_POP_SIZE,
    n_generations: int = DEFAULT_N_GENERATIONS,
    seed: int = DEFAULT_SEED,
) -> list[dict]:
    """
    Her n_cities değeri için QIGA ve klasik GA'yı çalıştırıp ölçüm sonuçlarını
    döndürür. Aynı seed her iki algoritmaya da verildiğinden (core.distance
    .generate_cities aynı tohumla çağrılır) ikisi de birebir aynı şehir
    koordinatları üzerinde çalışır — karşılaştırma adildir.
    """
    results: list[dict] = []

    for n_cities in n_cities_list:
        start = time.perf_counter()
        qiga_result = run_qiga(
            n_cities=n_cities, pop_size=pop_size, n_generations=n_generations, seed=seed
        )
        qiga_time = time.perf_counter() - start

        start = time.perf_counter()
        ga_result = run_classic_ga(
            n_cities=n_cities, pop_size=pop_size, n_generations=n_generations, seed=seed
        )
        ga_time = time.perf_counter() - start

        results.append(
            {
                "n_cities": n_cities,
                "qiga_distance": qiga_result.best_distance,
                "qiga_time": qiga_time,
                "ga_distance": ga_result.best_distance,
                "ga_time": ga_time,
            }
        )

    return results


def print_table(results: list[dict]) -> None:
    """Ölçüm sonuçlarını sabit genişlikli bir tablo olarak terminale yazdırır."""
    header = (
        f"{'n_cities':>8} | {'QIGA mesafe':>11} | {'QIGA süre(s)':>12} | "
        f"{'GA mesafe':>9} | {'GA süre(s)':>10} | {'Fark(%)':>8}"
    )
    print(header)
    print("-" * len(header))

    for row in results:
        # Fark(%): GA'ya göre QIGA ne kadar daha kısa/uzun bir tur buldu.
        # Pozitif değer → QIGA daha iyi (daha kısa mesafe).
        diff_pct = (row["ga_distance"] - row["qiga_distance"]) / row["ga_distance"] * 100

        print(
            f"{row['n_cities']:>8} | "
            f"{row['qiga_distance']:>11.2f} | "
            f"{row['qiga_time']:>12.4f} | "
            f"{row['ga_distance']:>9.2f} | "
            f"{row['ga_time']:>10.4f} | "
            f"{diff_pct:>+7.2f}%"
        )


def plot_benchmark(results: list[dict], output_path: str = DEFAULT_PLOT_PATH) -> None:
    """
    Benchmark sonuçlarını yan yana iki çizgi grafik olarak kaydeder:
      sol  : n_cities → en iyi mesafe (QIGA vs GA)
      sağ  : n_cities → çalışma süresi (QIGA vs GA)
    """
    n_cities = [row["n_cities"] for row in results]
    qiga_distances = [row["qiga_distance"] for row in results]
    ga_distances = [row["ga_distance"] for row in results]
    qiga_times = [row["qiga_time"] for row in results]
    ga_times = [row["ga_time"] for row in results]

    fig, (ax_dist, ax_time) = plt.subplots(1, 2, figsize=(11, 4.5), facecolor=_COLOR_SURFACE)

    for ax, qiga_y, ga_y, ylabel, title in (
        (ax_dist, qiga_distances, ga_distances, "En iyi mesafe", "n_cities vs. mesafe"),
        (ax_time, qiga_times, ga_times, "Süre (s)", "n_cities vs. süre"),
    ):
        ax.set_facecolor(_COLOR_SURFACE)
        ax.plot(
            n_cities, qiga_y, marker="o", markersize=8, linewidth=2,
            color=_COLOR_QIGA, label="QIGA",
        )
        ax.plot(
            n_cities, ga_y, marker="o", markersize=8, linewidth=2,
            color=_COLOR_GA, label="Klasik GA",
        )
        ax.set_xlabel("n_cities", color=_COLOR_INK)
        ax.set_ylabel(ylabel, color=_COLOR_INK)
        ax.set_title(title, color=_COLOR_INK)
        ax.set_xticks(n_cities)
        ax.grid(True, color=_COLOR_GRID, linewidth=1)
        ax.tick_params(colors=_COLOR_MUTED)
        for spine in ax.spines.values():
            spine.set_color(_COLOR_GRID)
        ax.legend(frameon=False, labelcolor=_COLOR_INK)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, facecolor=_COLOR_SURFACE, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    benchmark_results = run_benchmark()
    print_table(benchmark_results)
    plot_benchmark(benchmark_results)
