import os
import logging


class Config:
    LOG_FORMAT = '%(asctime)s %(levelname)8s %(engagement)s %(session)s %(message)s '
    LOG_LEVEL = logging.DEBUG
    DEBUG = False


class ProdConfig(Config):
    """Production configuration."""
    LOG_FORMAT = (
        '%(asctime)s %(levelname)8s %(engagement)s %(session)s %(funcName)20s'
        ' %(message)s %(type)s %(client)s %(user)s %(crud)s %(version)s'
    )
    LOG_LEVEL = logging.INFO


class DevConfig(Config):
    """Development configuration."""
    DEBUG = True


class TestConfig(Config):
    """Test configuration."""
    DEBUG = True


ENV_2_CONFIG = {'dev': DevConfig, 'test': TestConfig, 'prod': ProdConfig}


def runtime_config(config=None):
    if config is None:
        env = os.environ.get('APP_ENV', 'dev')
        assert env in ENV_2_CONFIG, 'Unknown APP_ENV value: ' + env
        config = ENV_2_CONFIG[env]
    return config
