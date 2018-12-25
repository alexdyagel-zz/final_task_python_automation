import enum

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Salesman(Base):
    __tablename__ = 'salesman'
    name = Column(String, primary_key=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Manager(Base):
    __tablename__ = 'manager'
    name = Column(String, primary_key=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Beverage(Base):
    __tablename__ = 'beverage'
    name = Column(String, primary_key=True)
    price = Column(Integer)

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return "{} price: {}".format(self.name, self.price)


class Ingredient(Base):
    __tablename__ = 'ingredient'
    name = Column(String, primary_key=True)
    price = Column(Integer)

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return "{} -- price: {}".format(self.name, self.price)


class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    name_salesman = Column(String, ForeignKey("salesman.name"), nullable=True)
    name_beverage = Column(String, ForeignKey("beverage.name"), nullable=True)
    name_ingredient = Column(String, ForeignKey("ingredient.name"), nullable=True)
    price = Column(Integer)

    def __init__(self, salesman, beverage, ingredient=None):
        self.name_salesman = salesman.name
        self.name_beverage = beverage.name
        if ingredient is not None:
            self.name_ingredient = ingredient.name

        price = 0
        if ingredient is not None:
            price += ingredient.price
        price += beverage.price
        self.price = price

    def __repr__(self):
        return "Salesman: {}\n Beverage: {}\n Ingredient: {}\n Total Price: {}".format(self.name_salesman,
                                                                                       self.name_beverage,
                                                                                       self.name_ingredient,
                                                                                       self.price)


@enum.unique
class UserType(enum.Enum):
    SALESMAN = Salesman
    MANAGER = Manager


@enum.unique
class ProductType(enum.Enum):
    BEVERAGE = Beverage
    INGREDIENT = Ingredient
