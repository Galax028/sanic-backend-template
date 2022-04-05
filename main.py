import glob
import importlib
import os
from textwrap import dedent

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
        logger.info("Initializing application...")

        for route in glob.glob("./routes/*.py"):
            if "__" in route:
                continue

            self.blueprint(
                importlib.import_module(route[2:-3].replace("/", ".")).router
            )
            logger.info(f"Registered route '{route}' successfully")

        for subfolder in glob.glob("./routes/*/"):
            if "__" in subfolder:
                continue

            logger.info(f"Detected route subfolder: {subfolder}")
            routes = []
            for route in glob.glob(f"{subfolder}*.py"):
                routes.append(
                    importlib.import_module(route[2:-3].replace("/", ".")).router
                )
                logger.info(f"Detected route '{route}' in '{subfolder}'")

            self.blueprint(
                Blueprint.group(
                    routes, url_prefix=f"/{os.path.basename(subfolder[:-1])}"
                )
            )
            logger.info(f"Registered route subfolder '{subfolder}' successfully")

        self.extend(
            config={
                "cors_origins": "*",
                "oas_ui_default": "swagger",
                "oas_ui_redoc": False,
            }
        )
        self.ext.openapi.describe(
            title="My Awesome API",
            version="1.0.0",
            description=dedent(
                """
            Welcome to my very awesome API!\n
            You can explore the different endpoints below in the docs.
            """
            ),
        )
        self.ext.openapi.add_security_scheme(
            ident="token",
            type="http",
            scheme="bearer",
            description="API bearer token authentication method",
        )

        self.run(
            host=self.config.HOST,
            port=self.config.PORT,
            dev=self.config.DEV_MODE,
            ssl=self.config.get("SSL_CERTS_FOLDER"),
            fast=not self.config.DEV_MODE,
            access_log=self.config.DEV_MODE,
        )


if __name__ == "__main__":
    uvloop.install()
    App()
