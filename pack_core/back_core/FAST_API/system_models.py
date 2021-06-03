from tortoise import fields, models
from MODS.standart_namespace.models import asf


class tortoise_state(models.Model):
    """
    Organizations
    """
    server = fields.CharField(description='Server name', max_length=31)
    pid = fields.CharField(description='PID on this server', max_length=13)
    state = fields.BooleanField(default=True)

    class Meta:
        table = asf('tortoise_state')
