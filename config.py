import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def get_database_uri():
        uri = os.environ.get('DATABASE_URL')
        if uri:
            return uri
        if os.environ.get('VERCEL'):
            return 'sqlite:////tmp/ielts.db'
        return 'sqlite:///' + os.path.join(basedir, 'ielts.db')

    @staticmethod
    def init_app(app):
        pass
