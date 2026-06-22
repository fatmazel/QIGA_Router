"""
Qubit-kodlu TSP kromozomu.

Her gen bir θ açısıyla temsil edilir (θ ∈ [0, π/2]).
  cos²(θ) : şehrin "erken" ziyaret edilme olasılığı
  sin²(θ) : şehrin "geç" ziyaret edilme olasılığı

Başlangıç: θ = π/4 → cos² = sin² = 0.5 → tam süperpozisyon (belirsizlik maksimum).
Algoritma ilerledikçe θ, en iyi bilinen çözüme doğru döner → belirsizlik azalır.
"""

import numpy as np


class QuantumChromosome:
    def __init__(self, n_cities: int, rng: np.random.Generator) -> None:
        self.n = n_cities
        # π/4: eşit süperpozisyon — her şehir başlangıçta eşit öncelikte
        self.theta = np.full(n_cities, np.pi / 4)

    def observe(self, rng: np.random.Generator) -> np.ndarray:
        """
        Qubit durumundan klasik bir rota örnekle (ölçüm / collapse).

        sin²(θ_i) her şehrin "geç ziyaret" skorudur.
        Küçük gürültü eklenerek eşit skorlarda rastgele sıra kırılır.
        argsort → küçük skor = erken ziyaret → geçerli TSP permütasyonu.
        """
        scores = np.sin(self.theta) ** 2          # her şehrin geç-ziyaret skoru
        noise = rng.uniform(0, 1e-6, size=self.n) # eşit skorlarda tie-breaking
        return np.argsort(scores + noise)          # shape (n,) — geçerli rota

    def rotate(self, best_route: np.ndarray, delta: float = 0.05) -> None:
        """
        Rotasyon kapısı: θ'yı en iyi bilinen çözüme doğru Δθ kadar döndür.

        best_route[k] = k. sırada ziyaret edilen şehir numarası
        rank_best[city] = bu şehrin best_route'taki sıra indeksi

        Kural:
          Eğer şehir best_route'ta mevcut pozisyonundan DAHA GEÇ gelmeli
            → sin²(θ) büyümeli → θ artar
          Eğer DAHA ERKEN gelmeli
            → sin²(θ) küçülmeli → θ azalır
          Eğer aynı sıradaysa
            → θ değişmez (zaten hizalı)
        """
        # best_route'ta her şehrin sıra indeksi
        rank_best = np.empty(self.n, dtype=int)
        rank_best[best_route] = np.arange(self.n)

        # Mevcut θ'dan üretilen sıra indeksi (gürültüsüz, deterministik)
        rank_current = np.argsort(np.sin(self.theta) ** 2)
        pos_current = np.empty(self.n, dtype=int)
        pos_current[rank_current] = np.arange(self.n)

        for city in range(self.n):
            if rank_best[city] > pos_current[city]:
                self.theta[city] += delta  # şehir daha geç gelmeli
            elif rank_best[city] < pos_current[city]:
                self.theta[city] -= delta  # şehir daha erken gelmeli
            # rank_best[city] == pos_current[city] → dokunma

        # θ'yı [0, π/2] aralığında tut
        self.theta = np.clip(self.theta, 0.0, np.pi / 2)
