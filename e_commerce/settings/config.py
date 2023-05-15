import datetime, os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

LOCAL_FOLDER = "/e-commerce/"

USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
SERVER = os.environ.get("SERVER")
DB = os.environ.get("DB")
PORT = os.environ.get("PORT")

#SQLALCHEMY_DATABASE_URI = 'sqlite:////local.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True

E_COMMERCE_DB = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, SERVER, PORT, DB)

SQLALCHEMY_BINDS = {
    'e_commerce': E_COMMERCE_DB
}

SECRET_KEY = "secret!"
SECURITY_PASSWORD_SALT = "secret!"
#JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=2)
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)

# # ADMIN
# ADMIN_USER = ""
# ADMIN_PASS = ""


# UPLOAD_FOLDER = ""
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
# MAX_CONTENT_LENGTH = 16 * 1024 * 1024


# # FLASK MAIL CONFIGURATION
# MAIL_SERVER = ""
# MAIL_PORT = 25
# MAIL_USE_TLS = True
# MAIL_USE_SSL = False
# MAIL_DEBUG = 0