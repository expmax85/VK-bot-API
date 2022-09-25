from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
            Pastry(title='Napoleon', image='napoleon.jpg'),
            Pastry(title='Praga', image='praga.jpg')
        ])

        categories[1].pastry.extend([
            Pastry(title='Levuve', image='levuve.jpg'),
            Pastry(title='Rafaello', image='rafaello.jpg'),
            Pastry(title='Ferrero', image='Ferrero.jpg')
        ])
        categories[2].pastry.extend([
            Pastry(title='Coca-Cola', image='Coca-Cola.jpg'),
            Pastry(title='Lipton-Tea', image='Lipton.jpg'),
            Pastry(title='Sprite', image='sprite.jpg')
        ])
        categories[3].pastry.extend([
            Pastry(title='Ice Cream', image='ice.jpg'),
            Pastry(title='Jelly', image='jelly.jpg')
        ])
        self.session.add_all(categories)
        self.session.commit()
        self.session.close()

    def get_categories(self) -> List:
        return self.session.query(Category).all()

    def get_goods_by_cty(self, cty: str) -> List:
        category_id = self.session.query(Category.id).filter(Category.name.like(cty)).one_or_none()[0]
        return self.session.query(Pastry).filter(Pastry.category_id == category_id).all()
