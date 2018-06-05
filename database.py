from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///tutorial.db', echo=True)
Base = declarative_base()


########################################################################
class User(Base):
    """"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    money = Column(Float, default=0)
    username = Column(String)
    password = Column(String)
    imagem = Column(String)

    # ----------------------------------------------------------------------
    def __init__(self, username, password, imagem):
        """"""
        self.username = username
        self.password = password
        self.imagem = imagem


class Status(Base):
    """"""
    __tablename__ = "status"
    id = Column(Integer, primary_key=True)
    tamagotchi_id = Column(Integer, ForeignKey("tamagotchis.id"), nullable=False)
    state = Column(String)

    def __init__(self, status, tamagotchi_id):
        self.state = status
        self.tamagotchi_id = tamagotchi_id


class Tamagotchi(Base):
    """"""
    __tablename__ = "tamagotchis"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String)
    name_pokemon = Column(String)
    birthday = Column(DateTime, default=datetime.now())
    last_update = Column(DateTime, default=datetime.now())
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


class Pokemon(Base):
    """"""
    __tablename__ = "pokemons"
    id = Column(Integer, primary_key=True)

    width = Column(String, default='80px')
    img = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    nome = Column(String)
    altura = Column(String)
    peso = Column(String)
    evolucao = Column(String)
    selected = Column(DateTime)

    cenario = Column(String, default='default')

    def __init__(self, img, width, nome, altura, peso, evolucao, user_id):
        """"""
        self.nome = nome
        self.img = img
        self.width = width
        self.altura = altura
        self.peso = peso
        self.evolucao = evolucao
        self.user_id = user_id
        self.selected = datetime.now()


# create tables
Base.metadata.create_all(engine)