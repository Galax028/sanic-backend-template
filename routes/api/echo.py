from auth import protected
from sanic import Blueprint
from sanic.exceptions import InvalidUsage
from sanic.request import Request
from sanic.response import HTTPResponse, json

router = Blueprint("echo", "/echo")


@router.get("/")
async def echo_index(request: Request) -> HTTPResponse:
    """Echo Endpoint

    This endpoint takes in a message and sends it back to the user

    openapi:
    ---
    tags:
      - echo
    parameters:
      - name: message
        in: query
        description: The message to be echoed
        required: true
        schema:
          type: string
          example: Hello, world!
    responses:
      "200":
        description: OK
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
              example:
                message: Hello, world!
    """
    message: str = request.args.get("message")
    if not message:
        raise InvalidUsage("You must provide a message to be echoed!", 400)

    return json({"message": message})


@router.get("/uppercase")
@protected
async def echo_uppercase(request: Request) -> HTTPResponse:
    """Echo To Uppercase Endpoint

    This endpoint takes in a message and sends it back to the user in uppercase

    openapi:
    ---
    tags:
      - echo
    security:
      - token: []
    parameters:
      - name: message
        in: query
        description: The message to be echoed back in uppercase
        required: true
        schema:
          type: string
          example: Hello, world!
    responses:
      "200":
        description: OK
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
              example:
                message: HELLO, WORLD!
    """
    message: str = request.args.get("message")
    if not message:
        raise InvalidUsage("You must provide a message to be echoed!", 400)

    return json({"message": message.upper()})
