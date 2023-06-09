from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# from flask_mail import Mail
from flask_jwt_extended import JWTManager

app = Flask(__name__)

cors = CORS(support_credentials=True)
db = SQLAlchemy()
# mail = Mail()
jwt = JWTManager()
api = Api()
