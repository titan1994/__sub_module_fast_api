"""
Автоподстановка моделей в конфигурацию черепахи
"""

import pkgutil
from os import walk

from GENERAL_CONFIG import GeneralConfig

DEFAULT_MODEL_FILE_NAME = 'models'
DEFAULT_PYDANTIC_FILE_NAME = 'pydmodel'


class TortoiseCFGModelError(Exception):
    pass


def models_inspector():
    """
    Основная функция формирования подстановки моделей.
    Папки с префиксами __ или _ игнорируются
    :return:
    """

    _, dirs, _ = next(walk(GeneralConfig.DEFAULT_AERICH_MODEL_APP_PATH))

    path_folder = []
    for name_dir in dirs:
        if name_dir.startswith('__') or name_dir.startswith('_'):
            continue

        path_folder.append(GeneralConfig.DEFAULT_AERICH_MODEL_APP_PATH / name_dir)

    if len(path_folder) == 0:
        raise TortoiseCFGModelError(f'{GeneralConfig.DEFAULT_AERICH_MODEL_APP_PATH} is empty!')

    result_model_path = []

    for pack in pkgutil.iter_modules(path=path_folder):
        if not pack.ispkg:
            continue

        if pack.name.startswith('__') or pack.name.startswith('_'):
            continue

        file_path = pack.module_finder.path / pack.name / f'{DEFAULT_MODEL_FILE_NAME}.py'
        if file_path.is_file():
            model_path = create_models_path(pack.module_finder.path.name, pack.name)
            result_model_path.append(model_path)

    return result_model_path


def create_models_path(parent, module):
    """
    Путь к модели по регламенту тортоиса

    :param parent:
    :param module:
    :return:
    """
    return f'{GeneralConfig.DEFAULT_AERICH_MODEL_PACK_PATH}.\
{GeneralConfig.DEFAULT_AERICH_MODEL_APP_PATH.name}.\
{parent}.{module}.\
{DEFAULT_MODEL_FILE_NAME}'
