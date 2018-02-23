import os

class Config:
    #get exported secret key or just assign it
    SECRET_KEY = os.environ.get('SECRET_KEY') or '#gfchyt678iui1224><>_'
    
    #initialise the application with config settings
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}