from pydantic import BaseSettings

class Settings(BaseSettings):

    db_name: str
    db_port: str
    db_password: str
    db_user: str
    db_host: str
    secret_key: str
    algorithm: str
    access_token_expire: str

    class Config:
        env_file = ".env"

    # db_user: str = 'db_user'
    # db_name: str = 'db_name'
    # db_password: str = 'password'
    # jwt_s: str = 'secret'
    # host: str = 'host'

settings = Settings()

