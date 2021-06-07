"""
Инициализация ядра Fast-API
"""

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from ...aerich_proc import config as cfg_tortoise
from ...RUN.__tools import fast_api_init
from . import system_routes
from ...system_models.system_models import tortoise_state
from os import getpid
from socket import gethostname
from GENERAL_CONFIG import GeneralConfig


app = FastAPI(title=GeneralConfig.PROJECT_NAME)

# Запуск с CORS
if GeneralConfig.CORS_WHITE_LIST:
    list_originals = GeneralConfig.CORS_WHITE_LIST.split(',')

    allow_credentials = False
    if GeneralConfig.CORS_ALLOW_CREDENTIALS:
        allow_credentials = True

    allow_methods = ['*']
    if GeneralConfig.CORS_ALLOW_METHODS:
        allow_methods = GeneralConfig.CORS_ALLOW_METHODS.split(',')

    allow_headers = ['*']
    if GeneralConfig.CORS_ALLOW_HEADERS:
        allow_headers = GeneralConfig.CORS_ALLOW_HEADERS.split(',')

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list_originals,
        allow_credentials=allow_credentials,
        allow_methods=allow_methods,
        allow_headers=allow_headers,
    )

# Запуск с ОРМ
if GeneralConfig.DEFAULT_DB_URI:
    GeneralConfig.TORTOISE_ORM = cfg_tortoise.get_tortoise_config()
    register_tortoise(
        app,
        GeneralConfig.TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )

# app.include_router(system_routes.router)

db = None  # для поддержки многофреймворочности
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
fast_api_init.register_all_routes_in_app(app)


@app.on_event("startup")
async def startup_event():
    await tortoise_state.get_or_create(server=gethostname(), pid=getpid())