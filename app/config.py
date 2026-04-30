import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///db/openers.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    LLM_MODEL = "claude-3-5-haiku-20241022"
    LLM_MAX_TOKENS = 1024
    OPENER_COUNT = 5  # jumlah kalimat pembuka yang di-generate


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

active_config = config_map.get(os.getenv("FLASK_ENV", "development"), DevelopmentConfig)
