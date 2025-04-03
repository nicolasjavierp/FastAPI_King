from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    species = Column(String)
    homeworld = Column(String)
    appearances = Column(String)
    affiliations = Column(String)
    locations = Column(String)
    dimensions = Column(String)
    weapons = Column(String)
    vehicles = Column(String)
    tools = Column(String)
