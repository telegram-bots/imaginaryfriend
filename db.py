import configparser


config = configparser.ConfigParser()
config.read('./main.cfg')

DATABASES = {'db': config['db']}
