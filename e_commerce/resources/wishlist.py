from flask import Blueprint
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful.reqparse import RequestParser
from e_commerce.models import UserModel, WishlistModel
from e_commerce.settings.exts import db

api_bp = Blueprint('api_wishlist', __name__)
api = Api(api_bp)


class WishlistResources(Resource):

    @jwt_required()
    def get(self):
        print("wishlist")
        id_user = get_jwt_identity()
        user = UserModel.find_by_id(id_user)
        cart_order_details = user.find_cart().order_details
        id_products_in_cart = [od.id_product for od in cart_order_details]
        wishlist = []
        for w in user.wishlist:
            wishlist_product = w.product.serialize()
            wishlist_product["in_cart"] = w.id_product in id_products_in_cart
            wishlist.append(wishlist_product)

        return { "wishlist": wishlist }, 200
    
    args_product = RequestParser()
    args_product.add_argument("id_product", type=int, required=True, help="id product")
    @jwt_required()
    def post(self):
        try:
            data = self.args_product.parse_args()
            id_user = get_jwt_identity()
            wishlist = WishlistModel.find_by_ids(id_user, data["id_product"])
            if not wishlist:
                new_wishlist = WishlistModel(id_user = id_user, id_product = data["id_product"])
                db.session.add(new_wishlist)
                db.session.commit()
                return { "message": "Product added to your wishlist" }, 200
            else:
                return { "message": "Product already on your wishlist" }, 200
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return { "message": str(e) }, 500
    
    @jwt_required()
    def delete(self):
        try:
            data = self.args_product.parse_args()
            id_user = get_jwt_identity()
            wishlist = WishlistModel.find_by_ids(id_user, data["id_product"])
            db.session.delete(wishlist)
            db.session.commit()
            return {}, 200
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return { "message": str(e) }, 500


api.add_resource(WishlistResources, '/e_commerce/wishlist')
