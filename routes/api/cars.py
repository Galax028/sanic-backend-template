from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, json

router = Blueprint("cars", "/cars")


@router.get("/get")
async def cars_get(request: Request) -> HTTPResponse:
    cars = ("Toyota", "Honda", "Volkswagen", "BMW", "Lamborghini")
    return json({"car": cars[int(request.args.get("id"))]})
