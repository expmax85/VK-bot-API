from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base
from config import DB_URL

engine = create_engine(DB_URL)
Base = declarative_base(bind=engine)


class Pastry(Base):
    __tablename__ = 'pastry'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String(80), nullable=False)
    description = Column('description', String(300))
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='pastry', cascade='all', lazy='joined')
    image = Column('image', String(80))

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
