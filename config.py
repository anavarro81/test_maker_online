import os
from dotenv import load_dotenv

load_dotenv() 

class Config:
    SECRET_KEY = "*W8Tr^g9UyM!sc8Uuuuc"


# Se crea la configuracion para desarrollo.
class DevelopmentConfig(Config):
    DEBUG = True
    # Parametros de conexion con la BBDD.
    # MYSQL_HOST = "localhost"
    # MYSQL_USER = "root"
    # MYSQL_PASSWORD = ""
    # MYSQL_DB = "preguntas"

    # # Parametros de conexion con la BBDD.
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB = os.environ.get('MYSQL_DB')



config = {"development": DevelopmentConfig}

my_config = DevelopmentConfig
print (f'MYSQL_HOST = {my_config.MYSQL_HOST}') 
print (f'MYSQL_USER = {my_config.MYSQL_USER}')
print (f'MYSQL_PASSWORD = {my_config.MYSQL_PASSWORD}')
print (f'MYSQL_DB = {my_config.MYSQL_DB}')