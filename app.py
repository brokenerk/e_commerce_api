from flask import Flask, jsonify
from e_commerce.settings.exts import db, cors, api, jwt
from e_commerce.settings.utils import ApiException
from e_commerce.resources.products import api_bp as api_products
from e_commerce.resources.cart import api_bp as api_cart
from e_commerce.resources.orders import api_bp as api_orders
from e_commerce.resources.users import api_bp as api_users
from e_commerce.resources.buy import api_bp as api_buy
from login import api_bp as api_login


def register_exts(app):
    db.init_app(app)
    cors.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    # mail.init_app(app)


def register_error_handlers(app):
    app.register_error_handler(ApiException, lambda err: err.to_result())


def register_blueprints(app):
    app.register_blueprint(api_login)
    app.register_blueprint(api_products)
    app.register_blueprint(api_cart)
    app.register_blueprint(api_orders)
    app.register_blueprint(api_users)
    app.register_blueprint(api_buy)



def create_app(config):
    app = Flask(__name__, template_folder="templates")
    app.config.from_pyfile(config)
    register_exts(app)
    register_error_handlers(app)
    register_blueprints(app)
    return app


app = create_app("e_commerce/settings/config.py")


@app.route("/")
def index():
    message = {'status': 200, 'message': 'Welcome'}
    resp = jsonify(message)
    resp.status_code = 200
    return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {'status': 404, 'message': 'Not Found'}
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.errorhandler(500)
def special_exception_handler(error):
    message = {'status': 500, 'message': 'Database Error'}
    resp = jsonify(message)
    resp.status_code = 500
    return resp




if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5115)
