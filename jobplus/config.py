class BaseConfig(object):
    SECRET_KEY = 'very secret key'
    #首页展示最新职位和公司的数量
    INDEX_PER_PAGE = 6
    ADMIN_PER_PAGE = 15


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    #设置数据库utf8编码,在数据库里新建jobplus数据库
    SQLALCHEMY_DATABASE_URI = ('mysql+mysqldb://root@localhost:3306/jobplus?charset=utf8')


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass

configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'test': TestingConfig
        }
