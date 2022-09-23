from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_URL
from database.models import Category, Pastry


class Database:

    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def insert_test_data(self) -> None:
        categories = [Category(name='Cakes'),
                      Category(name='Sweets'),
                      Category(name='Drink'),
                      Category(name='Other')]

        categories[0].pastry.extend([
            Pastry(title='Napoleon', image='12.jpg'),
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

    def get_categories(self) -> List:
        return self.session.query(Category).all()

    def get_goods_by_cty(self, cty: str) -> List:
        category_id = self.session.query(Category.id).filter(Category.name.like(cty)).one_or_none()[0]
        return self.session.query(Pastry).filter(Pastry.category_id == category_id).all()


db = Database(db_url=DB_URL)
