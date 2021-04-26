from fastapi import APIRouter
from MODS.rest_core.aerich_proc.mig import update_tables
from MODS.standart_namespace.routes import standardize_response

router = APIRouter(
    prefix="/migrations",
    tags=["pattern"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
@standardize_response
async def get():
    status = update_tables()
    return {'state': status}
