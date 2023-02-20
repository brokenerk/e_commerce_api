from flask import Blueprint
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful.reqparse import RequestParser
from e_commerce.models import UserModel, PersonModel, AccessModel
from e_commerce.settings.exts import db
from datetime import datetime

api_bp = Blueprint('api_users', __name__)
api = Api(api_bp)


class UsersResources(Resource):
    args_user = RequestParser()
    args_user.add_argument("tx_login", type=str, required=True, help="email")
    args_user.add_argument("tx_password", type=str, required=True, help="password")
    args_user.add_argument("tx_first_name", type=str, required=True, help="first name")
    args_user.add_argument("tx_last_name_a", type=str, required=True, help="last name A")
    args_user.add_argument("tx_last_name_b", type=str, required=True, help="last name B")
    args_user.add_argument("tx_street", type=str, required=True, help="street address")
    args_user.add_argument("tx_city", type=str, required=True, help="city address")
    args_user.add_argument("tx_state", type=str, required=True, help="state address")
    args_user.add_argument("tx_zipcode", type=str, required=True, help="zipcode address")
    args_user.add_argument("tx_telephone", type=str, required=True, help="telephone")


    @jwt_required()
    def get(self):
        id_user = get_jwt_identity()
        get_user = UserModel.find_by_id(id_user)
        user = get_user.serialize()
        user.update(get_user.person.serialize())
        return { "user": user }, 200
    
    
    def post(self):
        try:
            data = self.args_user.parse_args()

            new_user = UserModel(
                tx_login = data["tx_login"],
                tx_password = data["tx_password"]
            )
            del data["tx_login"]
            del data["tx_password"]

            new_person = PersonModel(**data)
            db.session.add(new_person)

            new_user.person = new_person
            db.session.add(new_user)
            db.session.commit()

            new_access = AccessModel(
                id_access = new_user.id_user,
                nu_attempt = 0
            )
            db.session.add(new_access)
            new_user.access = new_access

            db.session.commit()
            return {}, 200
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return { "message": str(e) }, 500
            

    @jwt_required()
    def put(self):
        try:
            data = self.args_user.parse_args()
            id_user = get_jwt_identity()
            
            users_dict = {
                "tx_login": data["tx_login"],
                "tx_password": data["tx_password"]
            }
            del data["tx_login"]
            del data["tx_password"]

            db.session.query(UserModel).filter(UserModel.id_user == id_user).update(users_dict)
            db.session.query(PersonModel).filter(PersonModel.id_person == id_user).update(data)
            db.session.commit()
            return {}, 200
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return { "message": str(e) }, 500


api.add_resource(UsersResources, '/e_commerce/users')
