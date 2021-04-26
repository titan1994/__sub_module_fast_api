"""
Основной файл для запуска ASGI сервера
"""

# Предпусковые операции
from MODS.rest_core.RUN.PRE_LAUNCH import APP_INIT

# Импорт приложения на запуск
from MODS.rest_core.back_core import app

