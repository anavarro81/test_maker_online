class Config:
    SECRET_KEY = "*W8Tr^g9UyM!sc8Uuuuc"


# Se crea la configuracion para desarrollo.
class DevelopmentConfig(Config):
    DEBUG = True
    # Parametros de conexion con la BBDD.
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = ""
    MYSQL_DB = "preguntas"


config = {"development": DevelopmentConfig}
