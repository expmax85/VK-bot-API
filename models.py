from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine("sqlite:///pastry_shop.db")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base(bind=engine)


class Pastry(Base):
    __tablename__ = 'pastry'

    id = Column('id', Integer, primary_key=True)
    title = Column('name', String(80), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='pastry', cascade='all', lazy='joined')

    def __repr__(self) -> str:
        return self.title


class Category(Base):
    __tablename__ = 'categories'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(30), nullable=False)
    pastry = relationship('Pastry', back_populates='category', lazy='joined')

    def __repr__(self) -> str:
        return self.name


def create_models():
    Base.metadata.create_all(bind=engine)
