class Config(object):
    """
    Common configurations
    """
    HOST = '0.0.0.0'
    PORT = 2002
    SECRET_KEY = 'p9Bv<3Eid9%$i01'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Admin!234@qa.rightinvoices.com/rightinvoices_db'
    #SQLALCHEMY_DATABASE_URI = 'mysql://prd_user:Cde34rfv$@ri-prd.ci0lm5djnoqp.ap-south-1.rds.amazonaws.com:3306/rightinvoices_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Put any configurations here that are common across all environments


class QaConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Admin!234@qa.rightinvoices.com/rightinvoices_db'
    DEBUG = True


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Admin!234@prd.rightinvoices.com/rightinvoices_db'
    DEBUG = False


app_config = {
    'dev': DevelopmentConfig,
    'qa': QaConfig,
    'prd': ProductionConfig,
    'master': ProductionConfig
}