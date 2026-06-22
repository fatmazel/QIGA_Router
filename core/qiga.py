"""
Quantum-Inspired Genetic Algorithm (QIGA) — TSP çözücü.

Algoritma adımları (Han & Kim, 2002 uyarlaması):
  1. Popülasyonu π/4 açılarıyla başlat  →  tam süperpozisyon
  2. Her nesil:
       a. Gözlem   : qubit kromozomlarından klasik rotalar örnekle
       b. Fitness  : her rotanın tur mesafesini hesapla
       c. Elitizm  : genel en iyi çözümü güncelle
       d. Rotasyon : her kromozomu en iyi bilinen çözüme doğru döndür
  3. Sonuç: en iyi rota, mesafe ve fitness geçmişi
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from core.chromosome import QuantumChromosome
from core.distance import compute_distance_matrix, generate_cities
from core.fitness import evaluate_population


@dataclass
class QIGAResult:
    best_route: list[int]           # en iyi tur sırası
    best_distance: float            # en kısa tur mesafesi
    fitness_history: list[float]    # her nesildeki en iyi mesafe (yakınsama grafiği)
    cities: list[list[float]]       # şehir koordinatları [[x, y], ...]


def run_qiga(
    n_cities: int = 10,
    pop_size: int = 20,
    n_generations: int = 100,
    delta: float = 0.05,
    seed: int = 42,
) -> QIGAResult:
    """
    QIGA'yı çalıştır ve en iyi TSP çözümünü döndür.

    n_cities     : şehir sayısı
    pop_size     : popülasyon büyüklüğü (qubit birey sayısı)
    n_generations: toplam nesil sayısı
    delta        : rotasyon kapısı adım boyutu (Δθ, radyan)
    seed         : tekrarlanabilirlik için rastgele tohum
    """
    rng = np.random.default_rng(seed)

    # ── Şehir koordinatları ve N×N mesafe matrisi ────────────────────────────
    coords = generate_cities(n_cities, seed=seed)
    dist_matrix = compute_distance_matrix(coords)

    # ── Popülasyon: tüm bireyler π/4 açısında başlar (tam süperpozisyon) ─────
    population = [QuantumChromosome(n_cities, rng) for _ in range(pop_size)]

    best_route: np.ndarray | None = None
    best_distance = float("inf")
    fitness_history: list[float] = []

    for _ in range(n_generations):
        # a. Gözlem: her qubit bireyin klasik rotasını örnekle
        routes = [chrom.observe(rng) for chrom in population]

        # b. Fitness: tüm rotaların tur mesafelerini hesapla
        distances = evaluate_population(routes, dist_matrix)

        # c. Bu neslin en iyisini global en iyi ile karşılaştır
        gen_best_idx = int(np.argmin(distances))
        if distances[gen_best_idx] < best_distance:
            best_distance = float(distances[gen_best_idx])
            best_route = routes[gen_best_idx].copy()

        fitness_history.append(best_distance)

        # d. Rotasyon kapısı: her bireyi global en iyiye doğru döndür
        for chrom in population:
            chrom.rotate(best_route, delta=delta)

    return QIGAResult(
        best_route=best_route.tolist(),
        best_distance=round(best_distance, 4),
        fitness_history=[round(d, 4) for d in fitness_history],
        cities=coords.tolist(),
    )
