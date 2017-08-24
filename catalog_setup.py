import os
import sys
import datetime
from sqlalchemy.sql import func
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    # Creates the 'user' table in the database
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

    # Serializes data into JSON format
    @property
    def serialize(self):
        return {
          'id': self.id,
          'name': self.name,
          'email': self.email,
        }


class Category(Base):
    # Creates the 'category' table in the database
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    image = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # Serializes data into JSON format
    @property
    def serialize(self):
        return {
            'name': self.name,
            'image': self.image,
            'id': self.id,
        }


class Item(Base):
    # Creates the 'item' table in the database
    __tablename__ = 'item'
    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(250))
    picture = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # Serializes data into JSON format
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'price': self.price,
            'picture': self.picture,
            'category_id': self.category_id,
            'time_created': self.time_created,
            'time_updated': self.time_updated,
            'user_id': self.user_id,
        }

engine = create_engine('postgresql:///catalog.db')

Base.metadata.create_all(engine)
