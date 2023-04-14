from flask import Blueprint, request
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful.reqparse import RequestParser
from e_commerce.models import ProductModel, UserModel, QuestionModel
from e_commerce.settings.exts import db
from datetime import datetime


api_bp = Blueprint('api_products', __name__)
api = Api(api_bp)

class ProductsResources(Resource):

    def get(self):
        search = request.args.get('search')
        get_products = ProductModel.find_all_products(search)
        products = [p.serialize() for p in get_products]
        return { "products": products }, 200
    

class ViewProductResources(Resource):

    def get(self, id):
        get_product = ProductModel.find_by_id(id)
        product = get_product.serialize()
        reviews = []
        stars = [0, 0, 0, 0, 0]
        for r in get_product.reviews:
            stars[r.stars - 1] += 1
            reviews.append(r.serialize())
        questions = [q.serialize() for q in get_product.questions]
        product["reviews"] = reviews
        product["questions"] = questions
        product["stars_array"] = stars
        return { "product": product }, 200
    
    args_question = RequestParser()
    args_question.add_argument("question", type=str, required=True, help="new question")
    def post(self, id):
        try:
            data = self.args_question.parse_args()

            new_question = QuestionModel(
                question = data["question"],
                id_product = id,
            )
            db.session.add(new_question)
            db.session.commit()

            return {}, 200
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return { "message": str(e) }, 500
        
    args_answer = RequestParser()
    args_answer.add_argument("answer", type=str, required=True, help="new answer")
    @jwt_required()
    def put(self, id):
        try:
            id_user = get_jwt_identity()
            data = self.args_answer.parse_args()

            question = QuestionModel.find_by_id(id)

            question.id_user = id_user
            question.answer = data["answer"]
            question.answer_date = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")

            db.session.commit()

            return {}, 200
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return { "message": str(e) }, 500

    

api.add_resource(ProductsResources, '/e_commerce/products')
api.add_resource(ViewProductResources, '/e_commerce/products/<int:id>')
