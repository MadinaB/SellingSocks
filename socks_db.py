from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Sock(Base):
    __tablename__ = 'sock'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    price = Column(Integer)
    description = Column(String(250))
    seller = Column(String(250))

    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'email': self.email,
                'picture': self.picture,
                'price': self.price,
                'description': self.description,
                'seller': self.seller, }


engine = create_engine('postgresql://socks:loveforsocks@localhost/sellingsocks')
Base.metadata.create_all(engine)
