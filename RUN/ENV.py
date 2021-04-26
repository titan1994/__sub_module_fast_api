"""
Загрузка переменных окружения.
Не всегда используется в начальной инициализации.
Иногда возникает необходимость вкинуть что-то своё в какую-либо библиотеку.
"""

from dotenv import load_dotenv
from pathlib import Path

from GENERAL_CONFIG import \
    GeneralConfig, AppMode

load_dotenv(GeneralConfig.PROJECT_GENERAL_FOLDER / '.env')

if GeneralConfig.DEFAULT_APP_MODE == AppMode.debug:
    load_dotenv(Path(GeneralConfig.PROJECT_GENERAL_FOLDER / '.env.development'))
else:
    load_dotenv(Path(GeneralConfig.PROJECT_GENERAL_FOLDER / '.env.production'))

ALL_ENV_LOAD = True

