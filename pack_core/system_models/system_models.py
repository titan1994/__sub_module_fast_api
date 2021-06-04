from tortoise import fields, models, Tortoise
from MODS.standart_namespace.models import asf
from socket import gethostname
from os import getpid
from ..aerich_proc import config as cfg_tortoise




class tortoise_state(models.Model):
    """
    Модель нужна, чтобы следить за состоянием конфигурации orm
    в каждом воркере.
    Если state = False - надо обновлять конфигурацию черепахи
    """
    server = fields.CharField(description='Server name', max_length=31)
    pid = fields.CharField(description='PID on this server', max_length=13)
    state = fields.BooleanField(default=True)

    class Meta:
        table = asf('tortoise_state')

    @classmethod
    async def state_check(cls) -> fields.BooleanField:
        """
        Для проверки статуса orm в процессе
        """
        obj = await cls.get(server=gethostname(), pid=getpid())
        return obj.state

    @classmethod
    async def state_activate(cls):
        obj = await cls.get(server=gethostname(), pid=getpid())
        await Tortoise.init(config=cfg_tortoise.get_tortoise_config())
        obj.state = True
        await obj.save()

    @classmethod
    async def state_reset(cls):
        await tortoise_state.all().update(state=False)