from e_commerce.settings.exts import db
from e_commerce.settings.helpers import BaseSerializer

class UserModel(db.Model, BaseSerializer):
    __tablename__ = "users"
    __bind_key__ = "e_commerce"

    fields = ['id_user', 'tx_login', 'tx_password']

    id_user = db.Column('id_user', db.Integer, db.ForeignKey("person.id_person"), primary_key=True, autoincrement=True)
    person = db.relationship("PersonModel", backref="users", lazy=True)
    tx_login = db.Column(db.String)
    tx_password = db.Column(db.String)


class PersonModel(db.Model, BaseSerializer):
    __tablename__ = "person"
    __bind_key__ = "e_commerce"

    fields = ['id_person', 'tx_first_name', 'tx_last_name_a', 'tx_last_name_b', 'tx_street' 'tx_city', 'tx_state','tx_zipcode','tx_telephone']

    id_person = db.Column('id_person', db.Integer, primary_key=True, autoincrement=True)
    tx_first_name = db.Column(db.String)
    tx_last_name_a = db.Column(db.String)
    tx_last_name_b = db.Column(db.String)
    tx_street = db.Column(db.String)
    tx_city = db.Column(db.String)
    tx_state = db.Column(db.String)
    tx_zipcode = db.Column(db.String)
    tx_telephone = db.Column(db.String)


class AccessModel(db.Model, BaseSerializer):
    __tablename__ = "access"
    __bind_key__ = "e_commerce"

    fields = ['id_access', 'nu_attempt', 'fh_failed', 'fh_lock']

    id_access = db.Column('id_access', db.Integer, db.ForeignKey("users.id_user"), primary_key=True, autoincrement=True)
    user = db.relationship("UserModel", backref="access", lazy=True)
    nu_attempt = db.Column(db.Integer)
    fh_failed = db.Column(db.DateTime)
    fh_lock = db.Column(db.DateTime)
    

class ProductModel(db.Model, BaseSerializer):
    __tablename__ = "product"
    __bind_key__ = "e_commerce"

    fields = ['id_product', 'tx_name', 'tx_description', 'ft_price', 'nu_stock', 'ft_discount', 'real_price']

    id_product = db.Column('id_product', db.Integer, primary_key=True, autoincrement=True)
    tx_name = db.Column(db.String)
    tx_description = db.Column(db.String)
    ft_price = db.Column(db.Float)
    nu_stock = db.Column(db.Integer)
    ft_discount = db.Column(db.Float)

    @property
    def real_price(self):
        return self.ft_price * (1 - (self.ft_discount * 0.01))

    @classmethod
    def find_all_products(cls):
        return cls.query.all()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(id_product = id).first()
    

class OrderDetailModel(db.Model, BaseSerializer):
    __tablename__ = "order_detail"
    __bind_key__ = "e_commerce"

    fields = ['id_product', 'id_order', 'nu_amount']

    id_product = db.Column('id_product', db.Integer, db.ForeignKey("product.id_product"), primary_key=True)
    id_order = db.Column('id_order', db.Integer, db.ForeignKey("order_c.id_order"), primary_key=True)
    nu_amount = db.Column(db.Integer)
    product = db.relationship("ProductModel", backref="order_detail", lazy=True)
    # order = db.relationship("OrderModel", backref="order_detail", lazy=True)
    

class OrderModel(db.Model, BaseSerializer):
    __tablename__ = "order_c"
    __bind_key__ = "e_commerce"

    fields = ['id_order', 'fh_date', 'st_purchased', 'ft_total', 'id_user']

    id_order= db.Column('id_order', db.Integer, primary_key=True)
    fh_date = db.Column(db.DateTime)
    st_purchased = db.Column(db.Boolean)
    ft_total = db.Column(db.Float)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id_user"))
    user = db.relationship("UserModel", backref="order_c", lazy=True)
    
