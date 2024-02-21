import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30)
    JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY")

class DevConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI').replace(
    'postgres://',
    'postgresql://',
    1
    )           
    SQLALCHEMY_TRACK_MODIFICATIONS=False


class TestConfig(Config):
    pass


class ProdConfig(Config):
    pass

config_dict={
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig
}

