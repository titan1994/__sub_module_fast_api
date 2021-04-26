from pkgutil import iter_modules
from importlib import import_module
from GENERAL_CONFIG import GeneralConfig


def init_from_func(folder_scripts, func_name):
    """
    Инициализация из скриптов, расположенных относительно корня проекта
    :param folder_scripts:
    :param func_name:
    :return:
    """

    for pack in iter_modules(path=[GeneralConfig.PROJECT_GENERAL_FOLDER / folder_scripts]):

        if pack.name.startswith('__') or pack.name.startswith('_'):
            continue

        mod = import_module(f'.{pack.name}', folder_scripts.replace('/', '.'))

        try:
            func = mod.__getattribute__(func_name)
            func()

        except Exception as exp:
            print(f'{folder_scripts}/{pack.name} import error!')
            print(exp)
