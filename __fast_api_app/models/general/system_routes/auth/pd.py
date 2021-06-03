from GENERAL_CONFIG import GeneralConfig
if getattr(GeneralConfig, 'SECRET_KEY', None): # Эти модели включаются, если в .env есть SECRET_KEY

    from .models import User
    from tortoise.contrib.pydantic import pydantic_model_creator


    User_Pydantic = pydantic_model_creator(User, name="User", exclude_readonly=True)
    UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

