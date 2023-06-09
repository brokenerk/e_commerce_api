from e_commerce.settings.exts import db
from e_commerce.settings.helpers import BaseSerializer
from sqlalchemy import or_
from sqlalchemy_filters import apply_pagination
from sqlalchemy.ext import mutable
import json

class JsonEncodedDict(db.TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""

    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return "{}"
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class UserModel(db.Model, BaseSerializer):
    __tablename__ = "users"
    __bind_key__ = "e_commerce"

    fields = ['id_user', 'tx_login', 'tx_password']

    id_user = db.Column('id_user',
                        db.Integer,
                        db.ForeignKey("person.id_person"),
                        db.ForeignKey("access.id_access"),
                        primary_key=True, 
                        autoincrement=True)
    tx_login = db.Column(db.String)
    tx_password = db.Column(db.String)
    person = db.relationship("PersonModel", backref="users", lazy=True)
    access = db.relationship("AccessModel", backref="users", lazy=True)
    orders = db.relationship("OrderModel", backref="users", lazy='dynamic', order_by="desc(OrderModel.fh_date)")
    wishlist = db.relationship("WishlistModel", backref="users", lazy='dynamic', order_by="WishlistModel.id_product")

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.id_user == id).first()
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter(cls.tx_login == username).first()

    def find_cart(self):
        for order in self.orders:
            if not order.st_purchased:
                return order
        return None

    def find_orders(self):
        orders = []
        for order in self.orders:
            if order.st_purchased:
                orders.append(order)
        return orders

class PersonModel(db.Model, BaseSerializer):
    __tablename__ = "person"
    __bind_key__ = "e_commerce"

    fields = ['id_person', 'tx_first_name', 'tx_last_name_a', 'tx_last_name_b', 'tx_street', 'tx_city', 'tx_state','tx_zipcode','tx_telephone']

    id_person = db.Column('id_person', db.Integer, primary_key=True, autoincrement=True)
    tx_first_name = db.Column(db.String)
    tx_last_name_a = db.Column(db.String)
    tx_last_name_b = db.Column(db.String)
    tx_street = db.Column(db.String)
    tx_city = db.Column(db.String)
    tx_state = db.Column(db.String)
    tx_zipcode = db.Column(db.String)
    tx_telephone = db.Column(db.String)

    def __init__(self, **kwargs):
        super(PersonModel, self).__init__(**kwargs)


class AccessModel(db.Model, BaseSerializer):
    __tablename__ = "access"
    __bind_key__ = "e_commerce"

    fields = ['id_access', 'nu_attempt', 'fh_failed', 'fh_lock']

    id_access = db.Column('id_access', db.Integer, primary_key=True, autoincrement=True)
    nu_attempt = db.Column(db.Integer)
    fh_failed = db.Column(db.DateTime)
    fh_lock = db.Column(db.DateTime)
    

class ProductModel(db.Model, BaseSerializer):
    __tablename__ = "product"
    __bind_key__ = "e_commerce"

    fields = ['id_product', 'tx_name', 'tx_description', 'ft_price', 'nu_stock', 'ft_discount', 'real_price', 'stars']

    id_product = db.Column('id_product', db.Integer, primary_key=True, autoincrement=True)
    tx_name = db.Column(db.String)
    tx_description = db.Column(db.String)
    ft_price = db.Column(db.Float)
    nu_stock = db.Column(db.Integer)
    ft_discount = db.Column(db.Float)
    reviews = db.relationship("ReviewModel", backref="product", lazy='dynamic', order_by="desc(ReviewModel.stars)")
    questions = db.relationship("QuestionModel", backref="product", lazy='dynamic', order_by="desc(QuestionModel.id_question)")

    @property
    def real_price(self):
        real_price = self.ft_price - (self.ft_price * (self.ft_discount / 100))
        return float("{:.2f}".format(real_price))

    @property
    def stars(self):
        stars = 0
        for r in self.reviews:
            stars += r.stars
        return float("{:.2f}".format(stars / self.reviews.count() if stars != 0 else stars))

    @classmethod
    def find_all_products(cls, search, page_number=None, page_size=None):
        search = search if search else ""
        page_number = int(page_number) if page_number else 1
        page_size = int(page_size) if page_size else 9

        products = cls.query.filter(
            or_(cls.tx_name.ilike("%" + search + "%"),
            cls.tx_description.ilike("%" + search + "%"))
        ).order_by(cls.id_product)

        products, pagination = apply_pagination(
            products, page_number=page_number, page_size=page_size
        )
        page_number, page_size, num_pages, total_results = pagination

        page_result = {
            "page_size": page_size,
            "page_number": page_number,
            "num_pages": num_pages,
            "total_results": total_results
        }
        return products.all(), page_result
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.id_product == id).first()
    
    def hasUserReview(self, id_user):
        for review in self.reviews:
            if (int(review.id_user) == int(id_user)):
                return True
        return False

class OrderDetailModel(db.Model, BaseSerializer):
    __tablename__ = "order_detail"
    __bind_key__ = "e_commerce"

    fields = ['id_product', 'id_order', 'nu_amount']

    id_product = db.Column('id_product', db.Integer, db.ForeignKey("product.id_product"), primary_key=True)
    id_order = db.Column('id_order', db.Integer, db.ForeignKey("order_c.id_order"), primary_key=True)
    nu_amount = db.Column(db.Integer)
    product = db.relationship("ProductModel", backref="order_detail", lazy=True)

    @classmethod
    def find_order_detail(cls, id_order, id_product):
        return cls.query.filter(cls.id_order == id_order, cls.id_product == id_product).first()
    

class OrderModel(db.Model, BaseSerializer):
    __tablename__ = "order_c"
    __bind_key__ = "e_commerce"

    fields = ['id_order', 'fh_date', 'st_purchased', 'ft_total', 'payment', 'id_user', 'total_formatted']

    id_order= db.Column('id_order', db.Integer, primary_key=True, autoincrement=True)
    fh_date = db.Column(db.DateTime)
    st_purchased = db.Column(db.Boolean)
    ft_total = db.Column(db.Float)
    payment = db.Column(JsonEncodedDict)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id_user"))
    order_details = db.relationship("OrderDetailModel", backref="order_c", lazy='dynamic', order_by="OrderDetailModel.id_product")

    @property
    def total_formatted(self):
        return float("{:.2f}".format(self.ft_total))

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.id_order == id).first()
    
    def add_product(self, id_product, amount):
        exists = False
        for od in self.order_details:
            product = od.product
            if id_product == product.id_product:
                exists = True
                print("----------->El producto ya esta en el carrito. No agregamos")
                break

        if not exists:
            try:
                new_od = OrderDetailModel(
                    id_order = self.id_order,
                    id_product = id_product,
                    nu_amount = amount
                )
                db.session.add(new_od)
            except Exception as e:
                db.session.rollback()
                print(str(e))
                print("Error al agregar producto al carrito")
            return True
        else:
            return False

    def update_amount(self, product, add):
        new_price = None
        try:
            new_amount = 0
            od = OrderDetailModel.find_order_detail(self.id_order, product.id_product)

            if add:
                print("------------->Incrementamos")
                new_amount = od.nu_amount + 1
                new_price = self.total_formatted + product.real_price
            else:
                print("------------->Decrementamos")
                new_amount = od.nu_amount - 1
                new_price = self.total_formatted - product.real_price
            
            # Si no hay cantidad, eliminamos producto
            if new_amount == 0:
                print("------------->Sin cantidad, eliminamos producto")
                self.remove_product(product.id_product)
            else:
                print("------------->Actualizamos cantidad")
                od.nu_amount = new_amount
                db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(str(e))
            print("Error al incrementar producto del carrito")

        return new_price

    def remove_product(self, id_product):
        try:
            od = OrderDetailModel.find_order_detail(self.id_order, id_product)
            db.session.delete(od)
        except Exception as e:
            db.session.rollback()
            print(str(e))
            print("Error al eliminar producto del carrito")
    
    def update_stock(self):
        for od in self.order_details:
            product = od.product
            product.nu_stock = product.nu_stock - od.nu_amount
        
    
class WishlistModel(db.Model, BaseSerializer):
    __tablename__ = "wishlist"
    __bind_key__ = "e_commerce"

    fields = ['id_user', 'id_product']

    id_user = db.Column('id_user', db.Integer, db.ForeignKey("users.id_user"), primary_key=True)
    id_product = db.Column('id_product', db.Integer, db.ForeignKey("product.id_product"), primary_key=True)
    product = db.relationship("ProductModel", backref="wishlist", lazy=True)

    @classmethod
    def find_by_ids(cls, id_user, id_product):
        return cls.query.filter(cls.id_user == id_user, cls.id_product == id_product).first()


class ReviewModel(db.Model, BaseSerializer):
    __tablename__ = "reviews"
    __bind_key__ = "e_commerce"

    fields = ['id_review', 'creation_date', 'country', 'stars', 'description', 'attachment', 'username']

    id_review = db.Column('id_review', db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime)
    country = db.Column(db.String)
    stars = db.Column(db.Integer)
    description = db.Column(db.String)
    attachment = db.Column(db.String)
    id_product = db.Column(db.Integer, db.ForeignKey("product.id_product"))
    id_user = db.Column(db.Integer, db.ForeignKey("users.id_user"))
    user = db.relationship("UserModel", backref="reviews", lazy=True)

    @property
    def username(self):
        splitted_login = self.user.tx_login.split('@')
        return splitted_login[0]


class QuestionModel(db.Model, BaseSerializer):
    __tablename__ = "questions"
    __bind_key__ = "e_commerce"

    fields = ['id_question', 'question', 'answer', 'answer_date', 'username']

    id_question = db.Column('id_question', db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    answer_date = db.Column(db.DateTime)
    id_product = db.Column(db.Integer, db.ForeignKey("product.id_product"))
    id_user = db.Column(db.Integer, db.ForeignKey("users.id_user"))
    user = db.relationship("UserModel", backref="questions", lazy=True)

    @property
    def username(self):
        splitted_login = self.user.tx_login.split('@')
        return splitted_login[0]

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.id_question == id).first()
    

mutable.MutableDict.associate_with(JsonEncodedDict)
