import random
import string

def random_string():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

class Config:
    SECRET_KEY = random_string()
    BASE_API_URL = "http://api.beta.dev.careerdream.org/core/v1/"

    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    DEBUG = True
    MYSQL_USER = "root"
    MYSQL_PASS = "214563"
    MYSQL_HOST = "localhost"
    MYSQL_PORT = "3306"
    MYSQL_DB = "psms"

config = {
    "default": ProductionConfig
}
