"""
Конфигурация черепашки для аерича. Пример того, что перменные среды нужно подгружать повторно
Так как аерич живёт своей жизнью отдельно от основного проекта
"""

from tortoise.backends.base.config_generator import expand_db_url


from ..RUN.__tools import tortoise as tools
from ..RUN import PRE_LAUNCH as PreLaunch

if PreLaunch.GeneralConfig.DEFAULT_DB_URI:
    TORTOISE_ORM = {
        "connections": {
            "default": expand_db_url(PreLaunch.GeneralConfig.DEFAULT_DB_URI, True)
        },
        "apps": {
            "models": {
                "models": ['aerich.models', *tools.models_inspector()],
                "default_connection": "default",
            }
        },
    }
else:
    TORTOISE_ORM = None
