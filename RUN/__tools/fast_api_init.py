import pkgutil
from os import walk
from importlib import import_module

from GENERAL_CONFIG import GeneralConfig

DEFAULT_ROUTER_FILE_NAME = 'routes'
DEFAULT_NAME_OF_ROUTER_OBJ = 'router'


class FastAPIRouteImportError(Exception):
    pass


def register_all_routes_in_app(app):
    """
    Регистрация всех роутов приложения
    :return:
    """

    _, dirs, _ = next(walk(GeneralConfig.DEFAULT_AERICH_MODEL_APP_PATH))

    path_folder = []
    for name_dir in dirs:
        if name_dir.startswith('__') or name_dir.startswith('_'):
            continue

        path_folder.append(GeneralConfig.DEFAULT_AERICH_MODEL_APP_PATH / name_dir)

    if len(path_folder) == 0:
        raise FastAPIRouteImportError(f'{GeneralConfig.DEFAULT_AERICH_MODEL_APP_PATH} is empty!')

    result_model_path = []

    for pack in pkgutil.iter_modules(path=path_folder):
        if not pack.ispkg:
            continue

        if pack.name.startswith('__') or pack.name.startswith('_'):
            continue

        file_path = pack.module_finder.path / pack.name / f'{DEFAULT_ROUTER_FILE_NAME}.py'
        if file_path.is_file():

            path_pack = generate_pack_name(pack.module_finder.path.name, pack.name)
            mod = import_module(
                f'.{DEFAULT_ROUTER_FILE_NAME}',
                path_pack
            )

            try:
                router = mod.__getattribute__(DEFAULT_NAME_OF_ROUTER_OBJ)
                if router is not None:
                    app.include_router(router)

            except Exception as exp:
                print(f'{path_pack} import error!')
                print(exp)

    return result_model_path


def generate_pack_name(par, ch):
    return \
        f'{GeneralConfig.DEFAULT_AERICH_MODEL_PACK_PATH}.{GeneralConfig.DEFAULT_AERICH_MODEL_APP_PATH.name}.{par}.{ch}'
