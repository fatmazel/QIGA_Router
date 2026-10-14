"""
Klasik Genetik Algoritma (GA) — TSP çözücü.

QIGA'nın karşılaştırma referansı: qubit kodlama ve rotasyon kapısı yerine
klasik permütasyon kromozomları, turnuva seçilimi, çaprazlama ve mutasyon
kullanılır. Algoritma adımları:
  1. Popülasyonu rastgele permütasyonlarla başlat
  2. Her nesil:
       a. Fitness  : her bireyin tur mesafesini hesapla
       b. Elitizm  : genel en iyi çözümü güncelle ve değiştirmeden aktar
       c. Seçilim  : turnuva seçilimiyle ebeveyn çiftleri belirle
       d. Çaprazlama: Order Crossover (OX1) ile çocuk üret
       e. Mutasyon : swap mutasyonu ile çeşitlilik koru
  3. Sonuç: en iyi rota, mesafe ve fitness geçmişi
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from core.distance import compute_distance_matrix, generate_cities
from core.fitness import evaluate_population


@dataclass
class GAResult:
    best_route: list[int]           # en iyi tur sırası
    best_distance: float            # en kısa tur mesafesi
    fitness_history: list[float]    # her nesildeki en iyi mesafe (yakınsama grafiği)
    cities: list[list[float]]       # şehir koordinatları [[x, y], ...]


def _tournament_selection(
    population: list[np.ndarray],
    distances: np.ndarray,
    tournament_size: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """
    Turnuva seçilimi: popülasyondan rastgele `tournament_size` birey seç,
    bunların arasında en düşük mesafeye (en iyi fitness'a) sahip olanı döndür.
    """
    contender_idx = rng.integers(0, len(population), size=tournament_size)
    winner_idx = contender_idx[np.argmin(distances[contender_idx])]
    return population[winner_idx]


def _order_crossover(
    parent_a: np.ndarray, parent_b: np.ndarray, rng: np.random.Generator
) -> np.ndarray:
    """
    Order Crossover (OX1): permütasyon kromozomları için klasik çaprazlama.

    Normal tek-noktalı çaprazlama permütasyonu bozar (aynı şehir iki kez
    görünebilir). OX1 bunu şöyle çözer:
      1. Rastgele bir [i, j) segmenti seç, parent_a'nın bu segmentini
         doğrudan çocuğa kopyala (göreli sırayı korur).
      2. Kalan pozisyonları parent_b'deki sırayla doldur; segmentte zaten
         var olan şehirleri atla. Böylece her şehir çocukta tam bir kez
         bulunur → geçerli bir TSP permütasyonu garanti edilir.
    """
    n = len(parent_a)
    i, j = sorted(rng.integers(0, n, size=2))

    child = np.full(n, -1, dtype=int)
    child[i:j] = parent_a[i:j]
    segment = set(child[i:j])

    fill_values = [city for city in parent_b if city not in segment]
    fill_positions = [pos for pos in range(n) if pos < i or pos >= j]
    for pos, city in zip(fill_positions, fill_values):
        child[pos] = city

    return child


def _swap_mutation(route: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """
    Swap mutasyonu: rotada rastgele iki pozisyonun yerini değiştir.
    Permütasyonu bozmadan (her şehir yine tam bir kez bulunur) çeşitlilik
    sağlayan en basit mutasyon operatörüdür.
    """
    mutated = route.copy()
    pos_a, pos_b = rng.integers(0, len(route), size=2)
    mutated[pos_a], mutated[pos_b] = mutated[pos_b], mutated[pos_a]
    return mutated


def run_classic_ga(
    n_cities: int = 10,
    pop_size: int = 20,
    n_generations: int = 100,
    seed: int = 42,
    crossover_rate: float = 0.8,
    mutation_rate: float = 0.1,
    tournament_size: int = 3,
) -> GAResult:
    """
    Klasik GA'yı çalıştır ve en iyi TSP çözümünü döndür.

    n_cities        : şehir sayısı
    pop_size        : popülasyon büyüklüğü
    n_generations   : toplam nesil sayısı
    seed            : tekrarlanabilirlik için rastgele tohum
    crossover_rate  : bir çiftin çaprazlanma olasılığı
    mutation_rate   : bir bireyin mutasyona uğrama olasılığı
    tournament_size : turnuva seçiliminde karşılaştırılan birey sayısı
    """
    rng = np.random.default_rng(seed)

    # ── Şehir koordinatları ve N×N mesafe matrisi (QIGA ile aynı seed → aynı problem) ──
    coords = generate_cities(n_cities, seed=seed)
    dist_matrix = compute_distance_matrix(coords)

    # ── Popülasyon: rastgele permütasyonlarla başlat ─────────────────────────
    population = [rng.permutation(n_cities) for _ in range(pop_size)]

    best_route: np.ndarray | None = None
    best_distance = float("inf")
    fitness_history: list[float] = []

    for _ in range(n_generations):
        # a. Fitness: tüm bireylerin tur mesafelerini hesapla
        distances = evaluate_population(population, dist_matrix)

        # b. Bu neslin en iyisini global en iyi ile karşılaştır (elitizm)
        gen_best_idx = int(np.argmin(distances))
        if distances[gen_best_idx] < best_distance:
            best_distance = float(distances[gen_best_idx])
            best_route = population[gen_best_idx].copy()

        fitness_history.append(best_distance)

        # c-e. Yeni popülasyonu oluştur: en iyi birey değişmeden aktarılır,
        #      kalanlar seçilim + çaprazlama + mutasyonla üretilir
        next_population = [best_route.copy()]
        while len(next_population) < pop_size:
            parent_a = _tournament_selection(population, distances, tournament_size, rng)
            parent_b = _tournament_selection(population, distances, tournament_size, rng)

            if rng.random() < crossover_rate:
                child = _order_crossover(parent_a, parent_b, rng)
            else:
                child = parent_a.copy()

            if rng.random() < mutation_rate:
                child = _swap_mutation(child, rng)

            next_population.append(child)

        population = next_population[:pop_size]

    return GAResult(
        best_route=best_route.tolist(),
        best_distance=round(best_distance, 4),
        fitness_history=[round(d, 4) for d in fitness_history],
        cities=coords.tolist(),
    )
