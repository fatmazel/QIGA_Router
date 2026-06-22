from fastapi import APIRouter

from api.models import SolveRequest, SolveResponse
from core.qiga import run_qiga

router = APIRouter()


@router.post("/solve", response_model=SolveResponse)
async def solve(req: SolveRequest) -> SolveResponse:
    """
    QIGA'yı tetikle ve en iyi TSP çözümünü döndür.

    Uzun çalışma sürelerinde (çok sayıda nesil/şehir) FastAPI'nin async yapısı
    event loop'u bloklamaz — ileride asyncio.to_thread ile sarılabilir.
    """
    result = run_qiga(
        n_cities=req.n_cities,
        pop_size=req.pop_size,
        n_generations=req.n_generations,
        delta=req.delta,
        seed=req.seed,
    )
    return SolveResponse(
        best_route=result.best_route,
        best_distance=result.best_distance,
        fitness_history=result.fitness_history,
        cities=result.cities,
        n_cities=req.n_cities,
        n_generations=req.n_generations,
        pop_size=req.pop_size,
    )
