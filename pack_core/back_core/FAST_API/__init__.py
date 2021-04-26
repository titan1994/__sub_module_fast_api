"""
Инициализация ядра Fast-API
"""

from fastapi import FastAPI
from GENERAL_CONFIG import GeneralConfig
from tortoise.contrib.fastapi import register_tortoise
from ...aerich_proc import config as cfg_tortoise
from ...RUN.__tools import fast_api_init
from . import system_routes

app = FastAPI(title=GeneralConfig.PROJECT_NAME)

if GeneralConfig.DEFAULT_DB_URI:
    register_tortoise(
        app,
        cfg_tortoise.TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )

app.include_router(system_routes.router)
fast_api_init.register_all_routes_in_app(app)

db = None  # для поддержки многофреймворочности
