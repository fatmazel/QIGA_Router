"""
Pydantic request/response şemaları — API giriş doğrulama ve çıktı yapısı.
"""

from pydantic import BaseModel, Field


class SolveRequest(BaseModel):
    n_cities: int = Field(default=10, ge=4, le=50, description="Şehir sayısı")
    pop_size: int = Field(default=20, ge=5, le=100, description="Popülasyon büyüklüğü")
    n_generations: int = Field(default=100, ge=10, le=1000, description="Nesil sayısı")
    delta: float = Field(default=0.05, gt=0.0, le=0.5, description="Rotasyon adım boyutu (Δθ)")
    seed: int = Field(default=42, description="Rastgele tohum")


class SolveResponse(BaseModel):
    best_route: list[int]
    best_distance: float
    fitness_history: list[float]
    cities: list[list[float]]
    n_cities: int
    n_generations: int
    pop_size: int


class CitiesRequest(BaseModel):
    n: int = Field(default=10, ge=2, le=100, description="Şehir sayısı")
    seed: int = Field(default=42, description="Rastgele tohum")


class CitiesResponse(BaseModel):
    cities: list[list[float]]
    distance_matrix: list[list[float]]
