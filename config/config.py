from dotenv import load_dotenv
import os

load_dotenv()


class Config(object):
    """
    Environment variables configuration class.
    """
    DEBUG = False

    SECRET_KEY = os.environ.get("SECRET_KEY", 'se%^&!70DCRETk*y')

    # SQLAlchemy variables
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgresql://yourusername:yourpassword@localhost/databasename')

    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT variables
    JWT_ACCESS_LIFESPAN = {os.environ.get('JWT_ACCESS_UNIT', 'minutes'): int(
        os.environ.get('JWT_ACCESS_VAL', 5))}
    JWT_REFRESH_LIFESPAN = {os.environ.get('JWT_REFRESH_UNIT', 'days'): int(
        os.environ.get('JWT_REFRESH_VAL', 30))}

    PORT = os.environ.get('PORT')
    HOST = os.environ.get('HOST')

    IS_DEV = os.environ.get('IS_DEV')
