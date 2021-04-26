from fastapi import APIRouter
from ...aerich_proc import mig
from MODS.standart_namespace.routes import standardize_response

router = APIRouter(
    prefix="/migrations",
    tags=["migration"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
@standardize_response
async def get():
    status = mig.update_tables()
    return {'state': status}
