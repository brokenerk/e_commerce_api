from e_commerce.settings.exts import db
from e_commerce.settings.helpers import BaseSerializer

class ProductModel(db.Model, BaseSerializer):
    __tablename__ = "product"
    __bind_key__ = "e_commerce"

    fields = ['id_product', 'tx_name', 'tx_description', 'ft_price', 'nu_stock', 'ft_discount']

    id_product = db.Column('id_product', db.Integer, primary_key=True, autoincrement=True)
    tx_name = db.Column(db.String)
    tx_description = db.Column(db.String)
    ft_price = db.Column(db.Float)
    nu_stock = db.Column(db.Integer)
    ft_discount = db.Column(db.Float)

    @classmethod
    def find_all_products(cls):
        return cls.query.all()
