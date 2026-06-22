"""
TSP fitness fonksiyonu: verilen rota için toplam tur mesafesi.

Rota: [c0, c1, ..., c_{n-1}] → c0→c1→...→c_{n-1}→c0 (kapalı döngü)
Minimize edilecek değer: toplam Öklid mesafesi.
"""

import numpy as np


def tour_distance(route: np.ndarray, dist_matrix: np.ndarray) -> float:
    """
    Rotanın toplam tur mesafesini hesapla.

    Son şehirden ilk şehre dönüş (i+1) % n indeksiyle sağlanır.
    """
    n = len(route)
    total = 0.0
    for i in range(n):
        city_from = route[i]
        city_to = route[(i + 1) % n]  # son şehirden başa döner
        total += dist_matrix[city_from, city_to]
    return total


def evaluate_population(routes: list, dist_matrix: np.ndarray) -> np.ndarray:
    """
    Tüm popülasyonun fitness değerlerini hesapla.
    Döndürür: shape (pop_size,) — her bireyin tur mesafesi.
    """
    return np.array([tour_distance(r, dist_matrix) for r in routes])
