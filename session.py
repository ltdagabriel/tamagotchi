# -*- coding: utf-8 -*-

from objetos import usuario, pokemon, tamagotchi
from database import *

engine = create_engine('sqlite:///tutorial.db', echo=False)


class Session:
    class __Session:
        def __init__(self):
            self.usuario = usuario.ListUsuario()

        def get_logged_user(self):
            return self.usuario.get_logged_user()

        def novo_usuario(self, username, password, imagem):
            return self.usuario.cadastro(username=username,
                                         password=password,
                                         imagem=imagem)

        def login(self, username, password):
            return self.usuario.login(username, password)

        def load_tamagotchi(self, by=None, value=None):
            tama = tamagotchi.ListTamagotchi()
            if by:
                return tama.load(by, value)
            else:
                return tama.load_all()

        def verify_if_exist(self, nome):
            tama = tamagotchi.ListTamagotchi()
            return tama.verify_if_exist(nome)

        def get_my_pokemons(self):
            poke = pokemon.ListPokemon()
            user = self.get_logged_user()
            if user:
                return poke.loadDatabase(user.id)
            return []

        def get_all_logged_user(self):
            return self.usuario.get_by_time(5)

        def logout(self):
            return self.usuario.logout()

    instance = None

    def __init__(self):
        if not Session.instance:
            Session.instance = Session.__Session()

    def __getattr__(self, item):
        return getattr(self.instance, item)
