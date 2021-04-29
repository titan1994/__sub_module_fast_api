"""
Мигратор АЕРИЧ
Загвостка была в том, что он очень хочет знать - что мы согласны чтобы он переименовал что-то или сделал.
Общительный в общем.
"""

import logging
from datetime import datetime

from MODS.scripts.python.cmd_run import run, run_with_answer
from MODS.scripts.python.easy_scripts import path_file_name_module
from GENERAL_CONFIG import GeneralConfig

DEFAULT_FILE_MIGRATION_LOG = GeneralConfig.PROJECT_GENERAL_FOLDER / '__migrations' / 'migration.log'

logging.basicConfig(
    filename=str(path_file_name_module(__name__, DEFAULT_FILE_MIGRATION_LOG)),
    filemode='a',
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)


class AerichMigrationError(Exception):
    pass


def update_tables():
    """
    Обновить все таблички по моделям - алембик сам умеет это делать.
    Не нужно говорить какие классы обновлять - велосипед...
    :return:
    """

    try:
        generate_script(datetime.now().isoformat())
        commit_change()
        return True

    except Exception as exp:
        logging.error(str(exp))

    return False


def generate_script(msg):
    """
    Создание скриптов миграции
    :return:
    """
    state, data = run_with_answer('aerich migrate')
    if not state == 0:
        raise AerichMigrationError(data)


def commit_change():
    """
    Запуск скриптов миграции
    :return:
    """
    state, data = run('aerich upgrade')
    if not state == 0:
        raise AerichMigrationError(data)
