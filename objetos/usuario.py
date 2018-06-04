# -*- coding: utf-8 -*-
from flask import session
from sqlalchemy.orm import sessionmaker
from session import *
from database import *
from datetime import datetime
from objetos import pokemon


class ObjetoUsuario:
    def __init__(self, user):
        self.user = user
        self.time = datetime.now()

    def update(self, user):
        self.user = user
        self.time = datetime.now()

    def to_json(self):
        user = {}
        for i in User.__table__.columns.keys():
            user.update({i: self.user.__getattribute__(i)})
        return {
            'time': self.time,
            'user': user
        }


class ListUsuario:
    class __ListUsuario:
        def __init__(self):
            self.usuario = []
            self.choice = [
                {
                    'img': 'ashe.png',
                    'nome': 'Ashe'
                },
                {
                    'img': 'brock.png',
                    'nome': 'Brock'
                },
                {
                    'img': 'carvalho.png',
                    'nome': 'Carvalho'
                },
                {
                    'img': 'gary.png',
                    'nome': 'Gary'
                },
                {
                    'img': 'james.png',
                    'nome': 'James'
                },
                {
                    'img': 'jessie.png',
                    'nome': 'Jessie'
                },
                {
                    'img': 'joy.png',
                    'nome': 'Joy'
                },
            ]

        def get_personagens(self):
            return self.choice

        def get_by_time(self, time):
            user = []
            for x in self.usuario:
                if (datetime.now() - x.time).total_seconds() < time:
                    user.append(x)
            return user

        def cadastro(self, username, password, imagem):
            s = sessionmaker(bind=engine)()
            user = User(username=username,
                        password=password,
                        imagem=imagem)
            s.add(user)
            s.commit()

            pokemons = pokemon.ListPokemon()

            pokemons.saveDatabase('Bulbasaur', user.id)
            pokemons.saveDatabase('Charmander', user.id)
            pokemons.saveDatabase('Squirtle', user.id)

            self.set_usuario(user)
            return True

        def set_usuario(self, usuario):
            user = list(filter(lambda x: x.user.id == usuario.id, self.usuario))
            if len(user):
                user[0].update(usuario)
            else:
                self.usuario.append(ObjetoUsuario(usuario))

        def get_logged_user(self):
            if 'username' in session:
                username = str(session.get('username'))
                user = list(sessionmaker(bind=engine)().query(User).filter(User.username.in_([username])))
                self.set_usuario(user[0])
                return user[0]
            else:
                return None

        def login(self, username, password):
            user = list(sessionmaker(bind=engine)().query(User).filter(User.username.in_([username]),
                                                                       User.password.in_([password])))
            if len(user):
                session['username'] = username
                return True
            return False

        def logout(self):
            #user = filter(lambda x: x.user.username == session['username'], self.usuario)
            #self.usuario.remove(user[0])
            session.pop('username', None)
            return True

    instance = None

    def __init__(self):
        if not ListUsuario.instance:
            ListUsuario.instance = ListUsuario.__ListUsuario()

    def __getattr__(self, item):
        return getattr(self.instance, item)


