"""
Начальная инициализация приложения.

Подгружаем переменные окружения,
выполняем необходимые миграции,
создаем удаляем папки/файлы

Всё это в зависимости от того какой выбран режим запуска Продуктив/Отладка и так далее

Самое важное - при импорте функций отсюда - загружаются/обновляются переменные окружения
"""

from os import environ, getcwd, getenv
from asyncio import get_event_loop
from pathlib import Path
from inspect import getfile as inspect_getfile
from shutil import copy as shutil_copy
import sys
from socket import gethostname

# Для докера и продакшн сборки без виртуального окружения - указать явно путь
sys.path.insert(0, getcwd())

from MODS.scripts.python.cmd_run import run
from MODS.scripts.python.jinja import jinja_render_to_file
from .__tools import pre_launch as launch_tools
from GENERAL_CONFIG import GeneralConfig, FastApiConfig


"""
Для воркеров и приложения - начальный момент запуска

Основная инициализация приложения - при каждом запуске,
в том числе и через воркеры (параллельные процессы, по настоящему параллельные)
"""

# env OK
from . import ENV as env_module

if env_module.ALL_ENV_LOAD:
    print('ENV LOAD')

# it's docker?
GeneralConfig.ITS_DOCKER = environ.get('ITS_DOCKER')
if GeneralConfig.ITS_DOCKER is None:
    GeneralConfig.ITS_DOCKER = False
    print('NO DOCKER RUN')
else:
    print('DOCKER RUN')

# data-base
if FastApiConfig in GeneralConfig.__bases__:
    """
    Общие настройки для всех проектов на фаст апи
    """

    # CORS
    GeneralConfig.CORS_WHITE_LIST = getenv('CORS_WHITE_LIST')
    if GeneralConfig.CORS_WHITE_LIST:
        print('ACTIVE FAST_API CORS')
    else:
        print('USE FAST_API WITHOUT CORS!')

    GeneralConfig.CORS_ALLOW_CREDENTIALS = getenv('CORS_ALLOW_CREDENTIALS')
    GeneralConfig.CORS_ALLOW_METHODS = getenv('CORS_ALLOW_METHODS')
    GeneralConfig.CORS_ALLOW_HEADERS = getenv('CORS_ALLOW_HEADERS')

    # Авторизация
    GeneralConfig.SECRET_KEY = getenv('SECRET_KEY')
    if GeneralConfig.SECRET_KEY:
        print('ACTIVE FAST_API AUTH WITH TOKEN')
    else:
        print('USE FAST_API WITHOUT AUTH!')

    # Докер не докер
    if GeneralConfig.ITS_DOCKER:
        DEFAULT_DB_URI = getenv('DATABASE_SETTINGS_URL_DOCKER')
    else:
        DEFAULT_DB_URI = getenv('DATABASE_SETTINGS_URL')

    # С базой данных или без
    if DEFAULT_DB_URI is None:
        print('USE FAST_API WITHOUT ORM TORTOISE!')
    else:
        print('ACTIVE FAST_API + ORM TORTOISE')
        if DEFAULT_DB_URI.startswith('postgresql'):
            DEFAULT_DB_URI = DEFAULT_DB_URI.replace('postgresql', 'postgres')

    GeneralConfig.DEFAULT_DB_URI = DEFAULT_DB_URI

# ADD - init
launch_tools.init_from_func(folder_scripts='__fast_api_app/init', func_name='first_init')

if FastApiConfig in GeneralConfig.__bases__ and GeneralConfig.DEFAULT_DB_URI:
    # Чтобы работал педантик и прочие радости

    from tortoise import Tortoise
    from .__tools import tortoise as tor_tools

    Tortoise.init_models(['aerich.models', *tor_tools.models_inspector()], 'models')

APP_INIT = True

"""
Отдельное приложение под названием "Предварительная инициализация". 
Зачем? ASGI слишком крут - и может порвать в щепки файловую систему. 
Поэтому всё что нужно сделать с файлами и даже с БД лучше делать заранее. 
Тоесть любая важная подготовка файлов - их интроспекция и первоначальные объекты в системе - 
создавать тут. 
"""


def pre_launch():
    """
    Отдельная инициализация от самого приложения -
    фактически именно в этом скрипте, запущенным ДО старта ASGI
    :return:
    """

    # MIGRATIONS (всегда статично и неизменно)
    if GeneralConfig.DEFAULT_DB_URI:
        migration_core_init()

    # Other (создаем файл по смыслу в папке launch и функцию first_run)
    launch_tools.init_from_func(folder_scripts='__fast_api_app/launch', func_name='first_run')


def migration_core_init():
    """
    Инициализация ядра мигратора
    :return:
    """
    if FastApiConfig in GeneralConfig.__bases__:
        migration_aerich_tortoise()

        # При наличии БД - вести состояние воркеров
        from ..system_models.system_models import tortoise_state
        get_event_loop().run_until_complete(tortoise_state.migration_clear_state_system())

    #
    # elif QuartApiConfig in GeneralConfig.__bases__:
    #     migration_alembic_gino()

    # else:
    #     ...


def migration_aerich_tortoise():
    """
    AERICH TORTOISE ORM FAST API
    """

    print('INIT AERICH CORE')

    from aerich.models import Aerich
    path = inspect_getfile(Aerich)
    with open(path, 'r+') as file:
        lines = file.readlines()
        if lines[-1].find('table') < 0:
            file.writelines(f"\n        table = '__{GeneralConfig.PROJECT_GENERAL_FOLDER.name}_aerich'")

    from aerich.cli import coro
    path = inspect_getfile(coro)

    cfg_import = GeneralConfig.DEFAULT_AERICH_CFG_PATH.replace('.TORTOISE_ORM', '')
    first_line = 'sys.path.insert(0, os.getcwd())'
    line_repair = f"{first_line}\nfrom importlib import import_module\nimport_module('{cfg_import}')\n"

    repair = False
    with open(path, 'r') as file:
        lines = file.readlines()
        if lines[4].find(first_line) < 0:
            lines.insert(4, line_repair)
            repair = True
    if repair:
        with open(path, 'w') as file:
            file.writelines(lines)

    if GeneralConfig.DEFAULT_AERICH_INI_FILE.is_file():
        # Проект уже успешно инициализирован, либо порезан

        if GeneralConfig.DEFAULT_AERICH_INI_PATH.is_file():
            print('AERICH WILL BE INIT EARLY')
        else:
            # Проект порезан. Это значит, что кто-то всё стёр на локальной машине
            print('AERICH REPAIR RUN')

            _, data_cmd = run(
                f'aerich init -t {GeneralConfig.DEFAULT_AERICH_CFG_PATH} --location {GeneralConfig.DEFAULT_AERICH_MIGR_PATH.absolute()}')
            print(data_cmd)

            _, data_cmd = run('aerich init-db')
            print(data_cmd)

            # Сохранение конфигурации (для последующего перемещения)
            shutil_copy(src=GeneralConfig.DEFAULT_AERICH_INI_FILE, dst=GeneralConfig.DEFAULT_AERICH_INI_PATH)
    else:
        if GeneralConfig.DEFAULT_AERICH_INI_PATH.is_file():
            # Перенос проекта куда-либо

            print('PROJECT WILL BE MOVE. RECOMBINE AERICH')
            shutil_copy(src=GeneralConfig.DEFAULT_AERICH_INI_PATH, dst=GeneralConfig.DEFAULT_AERICH_INI_FILE)
        else:
            # Первый старт
            print('AERICH FIRST RUN')

            _, data_cmd = run(
                f'aerich init -t {GeneralConfig.DEFAULT_AERICH_CFG_PATH} --location {GeneralConfig.DEFAULT_AERICH_MIGR_PATH.absolute()}')
            print(data_cmd)

            _, data_cmd = run('aerich init-db')
            print(data_cmd)

            # Сохранение конфигурации (для последующего перемещения)
            shutil_copy(src=GeneralConfig.DEFAULT_AERICH_INI_FILE, dst=GeneralConfig.DEFAULT_AERICH_INI_PATH)

    # Авто-рендер каждый раз из-за возможных переносов приложения между мирами
    src_jinja = Path(__file__).parent.parent / 'aerich_proc' / 'pattern_aerich_init.jinja'
    dict_jinja = {
        'tortoise_orm': GeneralConfig.DEFAULT_AERICH_CFG_PATH,
        'location': GeneralConfig.DEFAULT_AERICH_MIGR_PATH.absolute()
    }

    jinja_render_to_file(src=src_jinja, render=dict_jinja, dst=GeneralConfig.DEFAULT_AERICH_INI_PATH)
    jinja_render_to_file(src=src_jinja, render=dict_jinja, dst=GeneralConfig.DEFAULT_AERICH_INI_FILE)


if __name__ == '__main__':
    pre_launch()
