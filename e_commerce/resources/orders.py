from flask import Blueprint
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from e_commerce.models import UserModel, OrderModel

api_bp = Blueprint('api_orders', __name__)
api = Api(api_bp)


class OrdersResources(Resource):
    @jwt_required()
    def get(self):
        id_user = get_jwt_identity()
        user = UserModel.find_by_id(id_user)
        get_orders = user.find_orders()

        orders = [order.serialize() for order in get_orders]
        return { "orders": orders }, 200 
    
class ViewOrderResources(Resource):
    @jwt_required()
    def get(self, id_order):
        id_user = get_jwt_identity()
        order = {}
        get_order = OrderModel.find_by_id(id_order)
        
        if get_order:
            get_order_details = get_order.order_details

            order_details = []
            for order_detail in get_order_details:
                od = order_detail.serialize()
                od["product"] = order_detail.product.serialize()
                od["product"]["hasUserReview"] = order_detail.product.hasUserReview(id_user)
                order_details.append(od)

            order["order"] = get_order.serialize()
            order["order"]["order_details"] = order_details

        return order, 200
    

api.add_resource(OrdersResources, '/e_commerce/orders')
api.add_resource(ViewOrderResources, '/e_commerce/orders/<int:id_order>')

