#Fast-API - Действительно Fast 

Зарекомендовал себя как самый успешный фреймворк. 
Отлично сбалансирован. Действительно быстрый и есть Tortoise + pydantic + OpenAPI

#How to

Есть папка general - она очень важная. В ней собраны все модели и роуты. 
Модели разбросаны по папкам(группам)
Каждая группа содержит папки с моделями. 

```
general/essences/pattren - модель pattern
```

В этой конечной папке (pattern) должно быть 4-ре файла:

```
__init__.py  # - пустой
models.py  # - здесь объявляется класс модели ORM
pydantic.py  # - здесь объявляется класс pydantic из ORM
routes.py  # - здесь объявляются роуты, которые подхватывает свагер (опен-апи). 
```

(__init__.py, models.py) ОБЯЗАТЕЛЬНЫ. 

Другие папки и файлы - создавайте сколько влезет, это ничего не сломает. 
В том числе можно и в папке с 4-мя файлами сделать ещё папок и файлов.

#Про классы ORM
Обязательно добавляйте префикс через класс мета 
table = asf('pattern')

```
from tortoise import fields, models
from back_core.FAST_API.useful.models import asf


class Pattern(models.Model):
    """
    Pattern model
    """

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)

    class Meta:
        table = asf('pattern')

```