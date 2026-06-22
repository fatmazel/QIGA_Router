# QIGA-Router — Claude Code Bağlam Dosyası

## Proje Özeti

**QIGA-Router** (Quantum-Inspired Genetic Algorithm Router), klasik Gezgin Satıcı
Problemi'ni (TSP) ve araç rota problemini (VRP) çözen bir lojistik optimizasyon
sistemidir. Gerçek kuantum donanımı **kullanılmıyor** — literatürdeki gerçek bir
yaklaşım olan "Quantum-Inspired Evolutionary Algorithm (QIEA)" simüle ediliyor:
qubit-kodlu kromozomlar ve rotasyon kapıları, klasik bir genetik algoritma
çerçevesinde çalıştırılıyor.

Proje motivasyonu: CV ve mülakat portfolio'su.

---

## Mimari (3 Katman)

```
QIGA-Router/
├── core/          # Algoritma çekirdeği — Python, NumPy/SciPy, sıfırdan
├── api/           # FastAPI async endpoint'leri
├── frontend/      # React + React-Leaflet (harita) + Chart.js (canlı grafik)
├── tests/         # Birim ve entegrasyon testleri
└── docs/          # Mimari notlar, matematiksel türetmeler
```

### Katman 1 — Algoritma Çekirdeği (`core/`)
- Hazır optimizasyon kütüphanesi **kullanılmıyor**; matematik elle yazılıyor.
- Temel kavramlar:
  - **Qubit-kodlu kromozom**: Her gen, [0,1] aralığında bir olasılık açısı (θ) ile
    temsil edilir. Klasik bit'in süperpozisyon analogu.
  - **Rotasyon kapısı**: GA'nın "mutasyon" eşdeğeri. θ'yı küçük bir Δθ ile döndürerek
    arama uzayında yön değiştirir.
  - **Gözlem (collapse)**: θ değerinden klasik bir çözüm örneklenir (0 veya 1 kararı).
  - **Fitness fonksiyonu**: TSP toplam tur mesafesi (minimize).
  - **Seçilim**: Turnuva veya rulet-tekerleği seçimi.

### Katman 2 — API (`api/`)
- FastAPI, async endpoint'ler.
- Henüz geliştirilmedi (Hafta 2+).

### Katman 3 — Frontend (`frontend/`)
- React, React-Leaflet (harita görselleştirme), Chart.js (canlı fitness grafiği).
- Henüz geliştirilmedi (Hafta 3+).

---

## Haftalık Yol Haritası

| Hafta | Hedef |
|-------|-------|
| 1 | Klasik TSP + qubit-esinli GA çekirdeği (NumPy). Frontend/API yok. |
| 2 | FastAPI katmanı, algoritmanın HTTP üzerinden tetiklenmesi |
| 3 | React frontend, harita ve canlı grafik entegrasyonu |
| 4 | VRP uzantısı (çoklu araç), benchmark karşılaştırmaları |

---

## Geliştirici Rehberi

### Python Ortam Kurulumu

```bash
# Proje kökünde:
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

### Kodlama Kuralları (Bu Projede Geçerli)
- Matematiksel kısımlar (rotasyon kapısı, olasılık hesabı, fitness) **yorum satırlarıyla
  açıklanacak** — kullanıcının her satırı anlayabilmesi zorunlu.
- Büyük modüller yerine küçük, test edilebilir fonksiyonlar tercih edilecek.
- Her yeni modül eklendiğinde `tests/` altına karşılık gelen test dosyası açılacak.
- Hazır optimizasyon veya evolutionary computation kütüphanesi (DEAP, PyGAD vb.)
  **kullanılmayacak** — algoritma sıfırdan yazılıyor.

---

## Temel Teknik Kararlar (Bu Oturumda Alındı)

| Karar | Gerekçe |
|-------|---------|
| QIEA yaklaşımı, gerçek kuantum donanımı yok | Maliyet/pratiklik; literatürde kabul görmüş simülasyon yöntemi |
| NumPy/SciPy; hazır GA kütüphanesi yok | Mülakat için algoritmayı içselleştirmek şart |
| FastAPI (sync değil async) | Uzun süren optimizasyon çalışmaları için uygun |
| React-Leaflet | Açık kaynak, TSP rota görselleştirmesi için yeterli |

---

## Referans Literatür

- Han, K. H., & Kim, J. H. (2002). *Quantum-inspired evolutionary algorithm for a
  class of combinatorial optimization.* IEEE TEC.
- Zhang, G. (2011). *Quantum-inspired evolutionary algorithms: a survey and empirical
  study.* Journal of Heuristics.

---

_Bu dosya, yeni bir Claude oturumu açıldığında projeye hızla bağlam sağlamak için
otomatik olarak okunur. Önemli kararlar buraya eklenmelidir._
