from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from datetime import datetime
 
engine = create_engine('sqlite:///tutorial.db', echo=True)
Base = declarative_base()
 
########################################################################
class User(Base):
    """"""
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
 
    #----------------------------------------------------------------------
    def __init__(self, username, password):
        """"""
        self.username = username
        self.password = password
 
class Tamagotchi(Base):
    """"""
    __tablename__ = "tamagotchis"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String)
    name_pokemon = Column(String)
    birthday = Column(DateTime, default=datetime.now())
    last_update = Column(DateTime, default=datetime.now())
    state = Column(String, default='Saudavel')
    hunger = Column(Float, default=100.0) 
    happy = Column(Float, default=100.0) 
    health = Column(Float, default=100.0)
    
    def __init__(self, name, user_id, imagem):
        """"""
        self.name = name
        self.user_id = user_id
        self.last_update = datetime.now()
        self.birthday = datetime.now()
        self.name_pokemon = imagem
 


# create tables
Base.metadata.create_all(engine)