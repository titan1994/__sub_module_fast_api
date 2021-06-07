"""
Конфигурация черепашки для аерича. Пример того, что перменные среды нужно подгружать повторно
Так как аерич живёт своей жизнью отдельно от основного проекта
"""

from ..RUN import PRE_LAUNCH as PreLaunch


def get_tortoise_config():
    """
    От циклического импорта
    """
    return PreLaunch.get_tortoise_config()


if PreLaunch.GeneralConfig.DEFAULT_DB_URI:
    TORTOISE_ORM = get_tortoise_config()
else:
    TORTOISE_ORM = None
