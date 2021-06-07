"""
Нужно чтобы работал командный интерфейс аерика
"""

from .config import get_tortoise_config
TORTOISE_ORM = get_tortoise_config(True)

