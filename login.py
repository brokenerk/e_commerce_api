from flask import Blueprint, request
from flask_restful import Resource, Api
from datetime import timedelta
from e_commerce.settings.helpers import BaseSerializer
from e_commerce.models import UserModel
from flask_jwt_extended import create_access_token

api_bp = Blueprint("api_login", __name__)
api = Api(api_bp)

class Login(Resource, BaseSerializer):

    def post(self):
        data = request.get_json()
        username = data["username"]
        password = data["password"]

        logedUser = UserModel.find_by_username(username)

        if logedUser:

            if logedUser.tx_password == password:
                print("Usuario autenticado exitosamente")

                expires = timedelta(days=5)
                access_token = create_access_token(
                    identity = str(logedUser.id_user), 
                    expires_delta = expires
                )

                return {
                    'token': access_token,
                    'user': logedUser.serialize()
                }, 200
            else:
                print("Contraseña incorrecta")
                return { "message": "Password is wrong" }, 500
        else:
            print("Usuario no encontrado")
            return { "message": "Username is wrong" }, 500


api.add_resource(Login, '/e_commerce/login')
