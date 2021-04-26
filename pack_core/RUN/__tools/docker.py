from GENERAL_CONFIG import GeneralConfig, FastApiConfig


def get_command_to_run(windows_alternative=False):
    """
    Выбор команды запуска докер-файла, в зависимости от фреймворка

    Докер образы собираются для линукса (если требуется виндовский подход windows_alternative = True)
    Тоесть как тестировали - так и деплоим. Вцелом смысла в этом нет. uvloop точно быстрее asyncio
    """

    if FastApiConfig in GeneralConfig.__bases__:
        # FAST API - UVICORN

        if windows_alternative:
            command = f'CMD python APP_RUN/PRE_LAUNCH.py && uvicorn --host 0.0.0.0 --port {GeneralConfig.DEFAULT_PORT} ' + \
                      f'--workers {GeneralConfig.DEFAULT_WORKER_COUNT} APP_RUN.ZMAIN:app --reload'

        else:
            # Для конфигурации, совместимой с PyPy, используйте uvicorn.workers.UvicornH11Worker
            command = f'CMD python APP_RUN/PRE_LAUNCH.py && gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:{GeneralConfig.DEFAULT_PORT} ' + \
                      f'-w {GeneralConfig.DEFAULT_WORKER_COUNT} APP_RUN.ZMAIN:app --reload'

    return command
