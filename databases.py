from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Category, Pastry


class Database:

    def __init__(self):
        self.engine = create_engine("sqlite:///pastry_shop.db")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def insert_data(self):
        categories = [Category(name='Cakes'),
                      Category(name='Sweets'),
                      Category(name='Drink'),
                      Category(name='Other')]

        categories[0].pastry.extend([
            Pastry(title='Napoleon'),
            Pastry(title='Praga')
        ])
        categories[1].pastry.extend([
            Pastry(title='Levuve'),
            Pastry(title='Rafaello'),
            Pastry(title='Ferrero')
        ])
        categories[2].pastry.extend([
            Pastry(title='Coca-Cola'),
            Pastry(title='Lipton-Tea'),
            Pastry(title='Sprite')
        ])
        categories[3].pastry.extend([
            Pastry(title='Ice Cream'),
            Pastry(title='Gele')
        ])
        self.session.add_all(categories)
        self.session.commit()
        self.session.close()

    def get_categories(self):
        return self.session.query(Category).all()

    def get_goods_by_cty(self, cty):
        category_id = self.session.query(Category.id).filter(Category.name.like(cty)).one_or_none()[0]
        return self.session.query(Pastry).filter(Pastry.category_id == category_id).all()


db = Database()
