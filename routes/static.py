from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, file

router = Blueprint("static")
router.static("/assets", "../frontend/dist/assets")


@router.get("/")  # type: ignore
@router.get(r"/<_path:[^/api].*?>")
async def static_spa(_request: Request, _path: str = None) -> HTTPResponse:
    return await file("../frontend/dist/index.html")
