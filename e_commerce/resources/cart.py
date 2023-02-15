from flask import Blueprint
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful.reqparse import RequestParser
from e_commerce.models import UserModel, ProductModel, OrderModel
from e_commerce.settings.exts import db
from datetime import datetime

api_bp = Blueprint('api_cart', __name__)
api = Api(api_bp)


class CartResources(Resource):

    @jwt_required()
    def get(self):
        cart = {}
        id_user = get_jwt_identity()
        user = UserModel.find_by_id(id_user)
        get_cart = user.find_cart()

        if get_cart:
            get_order_details = get_cart.order_details

            order_details = []
            for order_detail in get_order_details:
                od = order_detail.serialize()
                od["product"] = order_detail.product.serialize()
                order_details.append(od)

            cart["cart"] = get_cart.serialize()
            cart["cart"]["order_details"] = order_details

        return cart, 200
    
    args_product = RequestParser()
    args_product.add_argument("id_product", type=int, required=True, help="id product")
    @jwt_required()
    def post(self):
        try:
            data = self.args_product.parse_args()
            id_product = data["id_product"]

            # Obtenemos el producto
            new_product = ProductModel.find_by_id(id_product)

            # Buscamos carrito y usuario
            id_user = get_jwt_identity()
            user = UserModel.find_by_id(id_user)
            cart = user.find_cart()

            first_time = False
            # Si no hay un carrito activo, lo agregamos
            if cart == None:
                cart = OrderModel(
                    fh_date = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S"),
                    ft_total = new_product.real_price,
                    id_user = id_user
                )
                db.session.add(cart)
                first_time = True
            
            # Intentamos agregar el producto
            added = cart.add_product(id_product, 1)

            # Si se agrego, actualizamos la orden, sino, acabamos. 
            # Tambien revisamos si es el primer articulo en el carrito
            if added and not first_time:
                cart.ft_total += new_product.real_price
            
            db.session.commit()
            return {}, 200
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return { "message": str(e) }, 500


    args_modify_amounts = RequestParser()
    args_modify_amounts.add_argument("id_product", type=int, required=True, help="id product")
    args_modify_amounts.add_argument("add", type=bool, required=True, help="increment or decrement product amount")
    @jwt_required()
    def put(self):
        try:
            data = self.args_modify_amounts.parse_args()
            id_product = data["id_product"]
            add = data["add"]

            # Buscamos carrito y usuario
            id_user = get_jwt_identity()
            user = UserModel.find_by_id(id_user)
            cart = user.find_cart()

            # Buscamos producto
            product = ProductModel.find_by_id(id_product)

            # Actualizamos la ordeDetail asociada
            new_price = cart.update_amount(product, add)

            # Actualizamos carrito
            cart.ft_total = new_price

            # Si no hay productos, borramos
            if cart.order_details == None:
                db.session.delete(cart)
            
            db.session.commit()
            return {}, 200
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return { "message": str(e) }, 500


    @jwt_required()
    def delete(self):
        try:
            data = self.args_product.parse_args()
            id_product = data["id_product"]
            
            # Buscamos carrito y usuario
            id_user = get_jwt_identity()
            user = UserModel.find_by_id(id_user)
            cart = user.find_cart()

            # Buscamos producto
            product = ProductModel.find_by_id(id_product)

            # Eliminamos orderDetail
            cart.remove_product(id_product)

            # Actualizamos la orden
            cart.ft_total -= product.real_price

            # Si no hay productos, borramos
            if cart.order_details == None:
                db.session.delete(cart)
            
            db.session.commit()
            return {}, 200
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return { "message": str(e) }, 500
        

api.add_resource(CartResources, '/e_commerce/cart')
