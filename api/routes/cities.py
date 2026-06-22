from fastapi import APIRouter

from api.models import CitiesRequest, CitiesResponse
from core.distance import compute_distance_matrix, generate_cities

router = APIRouter()


@router.post("/cities", response_model=CitiesResponse)
async def get_cities(req: CitiesRequest) -> CitiesResponse:
    """Rastgele şehir koordinatları ve mesafe matrisi üret."""
    coords = generate_cities(req.n, seed=req.seed)
    dist_matrix = compute_distance_matrix(coords)
    return CitiesResponse(
        cities=coords.tolist(),
        distance_matrix=dist_matrix.round(4).tolist(),
    )
