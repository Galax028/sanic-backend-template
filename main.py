import glob
import importlib

import ujson
import uvloop
from sanic import Blueprint, Sanic
from sanic.config import Config
from sanic.log import logger


class AppConfig(Config):
    def __init__(self):
        super().__init__()
        with open("./config.json") as f:
            self.update_config(ujson.load(f))


class App(Sanic):
    def __init__(self, *args, **kwargs):
        super().__init__("App", config=AppConfig(), *args, **kwargs)
        logger.info("[App]: Initializing application...")

        for route in glob.glob("./routes/*.py"):
            self.blueprint(
                importlib.import_module(route[2:-3].replace("/", ".")).router
            )
            logger.info(f"[App]: Successfully loaded route '{route}'")

        api_routes = []
        for api_route in glob.glob("./routes/api/*.py"):
            api_routes.append(
                importlib.import_module(api_route[2:-3].replace("/", ".")).router
            )
            logger.info(f"[App]: Successfully loaded API route '{api_route}'")

        self.blueprint(Blueprint.group(api_routes, url_prefix="/api"))

        self.run(
            host=self.config.HOST,
            port=self.config.PORT,
            debug=self.config.DEV_MODE,
            ssl=self.config.get("SSL_CERTS_FOLDER"),
            fast=not self.config.DEV_MODE,
            access_log=self.config.DEV_MODE,
        )


if __name__ == "__main__":
    uvloop.install()
    App()
