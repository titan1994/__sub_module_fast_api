"""
Импорт ядра
"""

from GENERAL_CONFIG import GeneralConfig, FastApiConfig

if FastApiConfig in GeneralConfig.__bases__:
    from .FAST_API import app as app
    from .FAST_API import db as db

