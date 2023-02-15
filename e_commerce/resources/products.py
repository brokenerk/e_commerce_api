from flask import Blueprint
from flask_restful import Resource, Api
from e_commerce.models import ProductModel


api_bp = Blueprint('api_products', __name__)
api = Api(api_bp)

class ProductsResources(Resource):

    def get(self):
        get_products = ProductModel.find_all_products()
        products = [p.serialize() for p in get_products]
        return {"products": products}, 200

api.add_resource(ProductsResources, '/e_commerce/products')
