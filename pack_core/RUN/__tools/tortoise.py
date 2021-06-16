"""
Автоподстановка моделей в конфигурацию черепахи
"""

import pkgutil
from os import walk
from GENERAL_CONFIG import GeneralConfig
from pathlib import Path

DEFAULT_MODEL_FILE_NAME = 'models'
DEFAULT_PYDANTIC_FILE_NAME = 'pydmodel'


class TortoiseCFGModelError(Exception):
    pass


def models_inspector():
    """
    Добавление моделей
    """
    models_inspector_one_path()

    if getattr(GeneralConfig, 'FAST_API_EXT_MODELS', None):
        for model in GeneralConfig.FAST_API_EXT_MODELS:
            models_inspector_one_path(
                path_to_routes=model['path'],
                path_to_pack=model['pack'],
                exclude_pack=model.get('excl_models', None)
            )


def models_inspector_one_path(
        path_to_routes=GeneralConfig.DEFAULT_AERICH_MODEL_APP_PATH,
        path_to_pack=GeneralConfig.DEFAULT_AERICH_MODEL_PACK_PATH,
        exclude_pack=None
):
    """
    Основная функция формирования подстановки моделей.
    Папки с префиксами __ или _ игнорируются
    :return:
    """

    _, dirs, _ = next(walk(path_to_routes))

    path_folder = []
    for name_dir in dirs:
        if name_dir.startswith('__') or name_dir.startswith('_'):
            continue

        path_folder.append(path_to_routes / name_dir)

    if len(path_folder) == 0:
        raise TortoiseCFGModelError(f'{path_to_routes} is empty!')

    result_model_path = []

    for pack in pkgutil.iter_modules(path=path_folder):
        if not pack.ispkg:
            continue

        if pack.name.startswith('__') or pack.name.startswith('_'):
            continue

        if exclude_pack:
            if pack.name in exclude_pack:
                continue

        file_path = pack.module_finder.path / pack.name / f'{DEFAULT_MODEL_FILE_NAME}.py'
        if file_path.is_file():
            model_path = create_models_path(
                parent=pack.module_finder.path.name,
                module=pack.name,
                path_to_routes=path_to_routes,
                path_to_pack=path_to_pack
            )
            result_model_path.append(model_path)

    # Системные модели
    from ...system_models import system_models
    obj_path = [el for el in Path(system_models.__file__).parts if el not in GeneralConfig.PROJECT_GENERAL_FOLDER.parts]
    path_to_system_model = '.'.join(obj_path)[:-3]  # убираем .py
    result_model_path.append(path_to_system_model)

    return result_model_path


def create_models_path(parent, module, path_to_routes, path_to_pack):
    """
    Путь к модели по регламенту тортоиса
    """
    return f'{path_to_pack}.\
{path_to_routes.name}.\
{parent}.{module}.\
{DEFAULT_MODEL_FILE_NAME}'
