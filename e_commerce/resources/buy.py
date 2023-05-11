from flask import Blueprint
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful.reqparse import RequestParser
from e_commerce.models import UserModel, WishlistModel
import e_commerce.paypal_api as paypal_api
from e_commerce.settings.exts import db
from datetime import datetime

api_bp = Blueprint('api_buy', __name__)
api = Api(api_bp)


class BuyResources(Resource):
    
    @jwt_required()
    def get(self):
        try:
            id_user = get_jwt_identity()
            user = UserModel.find_by_id(id_user)
            cart = user.find_cart()
            out_of_stock = []

            for od in cart.order_details:
                if(od.nu_amount > od.product.nu_stock):
                    out_of_stock.append(od.product.tx_name)
            
            if len(out_of_stock) > 0:        
                return {"message": "The products {} are out of stock. Try again later or reduce the amount".format(str(out_of_stock))}, 500
            else:
                paypal_order = paypal_api.createOrder(cart.order_details)
                return paypal_order, 200
        except Exception as e:
            print(str(e))
            return { "message": str(e) }, 500


    args_paypal_order_id = RequestParser()
    args_paypal_order_id.add_argument("paypal_order_id", type=str, required=True, help="id paypal api order")
    @jwt_required()
    def post(self):
        try:
            data = self.args_paypal_order_id.parse_args()
            paypal_order_id = data["paypal_order_id"]

            captureData = paypal_api.capturePayment(paypal_order_id)
            
            # Save paypal payment info
            id_user = get_jwt_identity()
            user = UserModel.find_by_id(id_user)
            cart = user.find_cart()
            cart.payment = captureData

            db.session.commit()
            return {}, 200
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return { "message": str(e) }, 500


    @jwt_required()
    def put(self):
        try:
            id_user = get_jwt_identity()
            user = UserModel.find_by_id(id_user)
            cart = user.find_cart()

            cart.st_purchased = True
            cart.fh_date = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
            cart.update_stock()

            # Remove purchased products from wishlist
            wishlist_id_products = [w.id_product for w in user.wishlist]
            for od in cart.order_details:
                if od.id_product in wishlist_id_products:
                    wishlist = WishlistModel.find_by_ids(id_user, od.id_product)
                    db.session.delete(wishlist)
                    db.session.commit()

            db.session.commit()
            return {}, 200
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return { "message": str(e) }, 500


api.add_resource(BuyResources, '/e_commerce/buy')