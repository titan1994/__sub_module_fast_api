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
    Регистрация роутов + дополнительные пути через конфиг
    """
    register_routes_in_app_from_path(app)

    if getattr(GeneralConfig, 'FAST_API_EXT_MODELS', None):
        for model in GeneralConfig.FAST_API_EXT_MODELS:
            register_routes_in_app_from_path(
                app,
                path_to_routes=model['path'],
                path_to_pack=model['pack'],
                exclude_pack=model.get('excl_routes', None),
                include_pack=model.get('incl_routes', None)
            )


def register_routes_in_app_from_path(
        app,
        path_to_routes=GeneralConfig.DEFAULT_AERICH_MODEL_APP_PATH,
        path_to_pack=GeneralConfig.DEFAULT_AERICH_MODEL_PACK_PATH,
        exclude_pack=None,
        include_pack=None
):
    """
    Регистрация всех роутов по заданному пути
    :return:
    """

    _, dirs, _ = next(walk(path_to_routes))

    path_folder = []
    for name_dir in dirs:
        if name_dir.startswith('__') or name_dir.startswith('_'):
            continue

        path_folder.append(path_to_routes / name_dir)

    if len(path_folder) == 0:
        raise FastAPIRouteImportError(f'{path_to_routes} is empty!')

    result_model_path = []

    for pack in pkgutil.iter_modules(path=path_folder):
        if not pack.ispkg:
            continue

        if pack.name.startswith('__') or pack.name.startswith('_'):
            continue

        if include_pack:
            if pack.name not in include_pack:
                continue

        elif exclude_pack:
            if pack.name in exclude_pack:
                continue

        file_path = pack.module_finder.path / pack.name / f'{DEFAULT_ROUTER_FILE_NAME}.py'
        if file_path.is_file():

            path_pack = generate_pack_name(
                par=pack.module_finder.path.name,
                ch=pack.name,
                path_to_pack=path_to_pack,
                path_to_routes=path_to_routes
            )
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


def generate_pack_name(par, ch, path_to_pack, path_to_routes):
    return \
        f'{path_to_pack}.{path_to_routes.name}.{par}.{ch}'
