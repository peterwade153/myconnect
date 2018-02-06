class Config(object):
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = 'not_secret_any_more'
	SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin@localhost/weconnect"

class ProductionConfig(Config):
	DEBUG = False

class StagingConfig(Config):
	DEVELOPMENT = True
	DEBUG = True

class DevelopmentConfig(Config):
	DEVELOPMENT = True
	DEBUG = True

class TestingConfig(Config):
	TESTING = True
	DEBUG=True
	SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin@localhost/testweconnect"