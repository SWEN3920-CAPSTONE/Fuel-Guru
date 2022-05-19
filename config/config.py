from dotenv import load_dotenv
import os

load_dotenv()


class Config(object):
    """
    Environment variables configuration class.
    """
    SECRET_KEY = os.environ.get("SECRET_KEY", 'se%^&!70DCRETk*y')

    # SQLAlchemy variables
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgresql://postgres@localhost/fuelgurudb')

    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT variables
    JWT_ACCESS_LIFESPAN = {os.environ.get('JWT_ACCESS_UNIT', 'minutes'): int(
        os.environ.get('JWT_ACCESS_VAL', 5))}
    JWT_REFRESH_LIFESPAN = {os.environ.get('JWT_REFRESH_UNIT', 'days'): int(
        os.environ.get('JWT_REFRESH_VAL', 30))}

    PORT = int(os.environ.get('PORT',9000))
    HOST = os.environ.get('HOST', '0.0.0.0')

    IS_DEV = os.environ.get('IS_DEV', 'False') == 'True'
    
    
    MAIL_SERVER=os.environ.get('MAIL_SERVER','localhost')    
    MAIL_PORT= int(os.environ.get('MAIL_PORT',25))    
    MAIL_USE_TLS= os.environ.get('MAIL_USE_TLS','False') == 'True'
    MAIL_USE_SSL=os.environ.get('MAIL_USE_SSL','False') == 'True'
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER=os.environ.get('MAIL_DEFAULT_SENDER')
    
    TESTING=os.environ.get('TESTING','False') == 'True'

    API_KEY = os.environ.get('API_KEY')
    URL = os.environ.get('URL')
    URL_ROUTE = os.environ.get('URL_ROUTE')
