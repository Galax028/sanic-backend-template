from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, json

router = Blueprint("echo", "/echo")


@router.get("/")
async def echo_index(request: Request) -> HTTPResponse:
    return json({"message": request.args.get("message")})
