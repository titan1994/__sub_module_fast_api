"""
Конфигурация черепашки для аерича. Пример того, что перменные среды нужно подгружать повторно
Так как аерич живёт своей жизнью отдельно от основного проекта
"""

from tortoise.backends.base.config_generator import expand_db_url
from ..RUN.__tools import tortoise as tools
from GENERAL_CONFIG import GeneralConfig


def get_tortoise_config(use_import=False):
    """

    """
    if use_import:
        from ..RUN.PRE_LAUNCH import APP_INIT

    DEFAULT_DB_URI = GeneralConfig.DEFAULT_DB_URI
    if DEFAULT_DB_URI:
        return {
            "connections": {
                "default": expand_db_url(DEFAULT_DB_URI, True)
            },
            "apps": {
                "models": {
                    "models": ['aerich.models', *tools.models_inspector()],
                    "default_connection": "default",
                }
            },
        }
    return None


TORTOISE_ORM = get_tortoise_config(False)



