class Config:
    SECRET_KEY = 'JYXTYFZX'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAX_CONTENT_LENGTH = 30 * 1024 * 1024

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123@localhost:3306/jyxtyf'
    DEBUG = True


config = {
    'default': DevelopmentConfig
}
