"""
TSP için şehir koordinatları ve mesafe matrisi.

Terminoloji:
  n         : şehir sayısı
  coords    : (n, 2) boyutlu NumPy dizisi — her satır bir şehrin (x, y) koordinatı
  dist_matrix: (n, n) boyutlu simetrik matris — dist_matrix[i][j] = şehir i'den j'ye mesafe
"""

import numpy as np
from scipy.spatial.distance import cdist


def generate_cities(n: int, seed: int = 42) -> np.ndarray:
    """
    n adet şehri [0, 100] x [0, 100] düzleminde rastgele üret.

    seed parametresi: aynı tohum → aynı şehir konumları → tekrarlanabilir deney.
    Mülakata gidersen "seed=42 ile sonuçlarım şöyle" diyebilirsin.

    Döndürür: shape (n, 2) — [[x0,y0], [x1,y1], ...]
    """
    rng = np.random.default_rng(seed)          # modern NumPy rastgele üreteci
    return rng.uniform(0, 100, size=(n, 2))    # (n, 2) uniform dağılım


def compute_distance_matrix(coords: np.ndarray) -> np.ndarray:
    """
    Koordinat dizisinden N×N Öklid mesafe matrisi hesapla.

    scipy.cdist kullanıyoruz: her çift (i, j) için √[(xi-xj)² + (yi-yj)²]
    'euclidean' metriği bu formülü vektörize biçimde hesaplar — Python döngüsünden
    çok daha hızlı.

    Matris özellikleri:
      - Simetrik      : dist[i][j] == dist[j][i]
      - Köşegen sıfır : dist[i][i] == 0
    """
    return cdist(coords, coords, metric='euclidean')  # (n, n) matris döner


def city_info(coords: np.ndarray, dist_matrix: np.ndarray) -> None:
    """Debug / görselleştirme: temel bilgileri yazdır."""
    n = len(coords)
    print(f"Şehir sayısı : {n}")
    print(f"Koordinatlar (ilk 5):\n{coords[:5]}")
    print(f"Mesafe matrisi (ilk 3x3):\n{dist_matrix[:3, :3].round(2)}")
    print(f"En kısa kenar: {dist_matrix[dist_matrix > 0].min():.2f}")
    print(f"En uzun kenar: {dist_matrix.max():.2f}")
