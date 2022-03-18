from pydantic import BaseSettings

class Settings(BaseSettings):

    db_user: str = 'db_user'
    db_name: str = 'db_name'
    db_password: str = 'password'
    jwt_s: str = 'secret'
    host: str = 'host'

settings = Settings()