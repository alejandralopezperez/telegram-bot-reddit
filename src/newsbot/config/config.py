from pydantic_settings import BaseSettings


class AppConfiguration(BaseSettings):
    nbt_access_token: str
    user_agent: str
    update_period: int
    last_updated_folder: str

    class Config:
        env_file = '.env'
        