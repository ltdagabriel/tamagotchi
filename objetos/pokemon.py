from sqlalchemy.orm import sessionmaker
from database import *
from session import *
from objetos import usuario


class ObjetoPokemon:
    def __init__(self, pokemon):
        self.pokemon = pokemon


    def to_json(self):
        pokemon = {}
        for i in Pokemon.__table__.columns.keys():
            pokemon.update({i: self.pokemon.__getattribute__(i)})

        return pokemon


class ListPokemon:
    class __ListPokemon:
        def __init__(self):
            self.loja = [
                {'nome': 'Lugia', 'price': 500.0},
                {'nome': 'Mewtwo', 'price': 700.0},
                {'nome': 'Onix', 'price': 100.0},
                {'nome': 'Pichu', 'price': 100.0},
                {'nome': 'Munchlax', 'price': 100.0},
                {'nome': 'Latias', 'price': 500.0},
                {'nome': 'Latios', 'price': 500.0},
                {'nome': 'Lapras', 'price': 200.0},
                {'nome': 'Teddiursa', 'price': 50.0},
                {'nome': 'Wailmer', 'price': 50.0},
                {'nome': 'Aerodactyl', 'price': 350.0},
                {'nome': 'Mareep', 'price': 50.0}
            ]

            self.pokemons = [
                {
                    'img': "Bulbasaur.gif",
                    'width': '120px',
                    'nome': 'Bulbasaur',
                    'time': 30 * 60,
                    'evolucao': 'Ivysaur',
                    'peso': '6.9 Kg',
                    'altura': '0.7 m'
                },
                {
                    'img': "ivysaur.gif",
                    'width': '150px',
                    'nome': 'Ivysaur',
                    'time': 60 * 60,
                    'evolucao': 'Venusaur',
                    'peso': '13.0 Kg',
                    'altura': '1.0 m'
                },
                {
                    'img': "venusaur.gif",
                    'width': '200px',
                    'nome': 'Venusaur',
                    'evolucao': None,
                    'peso': '100.0 Kg',
                    'altura': '2.0 m'
                },
                {
                    'img': "charmander.gif",
                    'width': '130px',
                    'nome': 'Charmander',
                    'time': 30 * 60,
                    'evolucao': 'Charmeleon',
                    'peso': '8.5 Kg',
                    'altura': '0.6 m'
                },
                {
                    'img': "charmeleon.gif",
                    'width': '150px',
                    'nome': 'Charmeleon',
                    'time': 60 * 60,
                    'evolucao': 'Charizard',
                    'peso': '19.0 Kg',
                    'altura': '1.1 m'
                },
                {
                    'img': "charizard.gif",
                    'width': '200px',
                    'nome': 'Charizard',
                    'evolucao': None,
                    'peso': '90.5 Kg',
                    'altura': '1.7 m'
                },
                {
                    'img': "squirtle.gif",
                    'width': '130px',
                    'nome': 'Squirtle',
                    'time': 30 * 60,
                    'evolucao': 'Wartortle',
                    'peso': '9.0 Kg',
                    'altura': '0.5 m'
                },
                {
                    'img': "wartortle.gif",
                    'width': '150px',
                    'nome': 'Wartortle',
                    'time': 60 * 60,
                    'evolucao': 'Blastoise',
                    'peso': '22.5 Kg',
                    'altura': '1.0 m'
                },
                {
                    'img': "blastoise-mega.gif",
                    'width': '170px',
                    'nome': 'Blastoise',
                    'evolucao': None,
                    'peso': '85.5 Kg',
                    'altura': '1.6 m'
                },
                {
                    'img': "blastoise-mega.gif",
                    'width': '170px',
                    'nome': 'Blastoise',
                    'evolucao': None,
                    'peso': '85.5 Kg',
                    'altura': '1.6 m'
                },
                {
                    'img': "lugia.gif",
                    'width': '170px',
                    'nome': 'Lugia',
                    'evolucao': None,
                    'peso': '216.0 Kg',
                    'altura': '5.2 m'
                },
                {
                    'img': "mewtwo.gif",
                    'width': '130px',
                    'nome': 'Mewtwo',
                    'evolucao': None,
                    'peso': '122.0 Kg',
                    'altura': '2.0 m'
                },
                {
                    'img': "onix.gif",
                    'width': '130px',
                    'nome': 'Onix',
                    'evolucao': 'Steelix',
                    'peso': '210.0 Kg',
                    'altura': '8.8 m'
                },
                {
                    'img': "steelix.gif",
                    'width': '150px',
                    'nome': 'Steelix',
                    'evolucao': None,
                    'peso': '400.0 Kg',
                    'altura': '9.2 m'
                },
                {
                    'img': "pichu.gif",
                    'width': '100px',
                    'nome': 'Pichu',
                    'evolucao': "Pikachu",
                    'peso': '2.0 Kg',
                    'altura': '0.3 m'
                },
                {
                    'img': "pikachu.gif",
                    'width': '130px',
                    'nome': 'Pikachu',
                    'evolucao': "Raichu",
                    'peso': '6.0 Kg',
                    'altura': '0.4 m'
                },
                {
                    'img': "raichu-3.gif",
                    'width': '150px',
                    'nome': 'Raichu',
                    'evolucao': None,
                    'peso': '30.0 Kg',
                    'altura': '0.8 m'
                },
                {
                    'img': "munchlax.gif",
                    'width': '100px',
                    'nome': 'Munchlax',
                    'evolucao': 'Snorlax',
                    'peso': '105.0 Kg',
                    'altura': '0.6 m'
                },
                {
                    'img': "snorlax.gif",
                    'width': '200px',
                    'nome': 'Snorlax',
                    'evolucao': None,
                    'peso': '460.0 Kg',
                    'altura': '2.1 m'
                },
                {
                    'img': "wailmer.gif",
                    'width': '150px',
                    'nome': 'Wailmer',
                    'evolucao': 'Wailord',
                    'peso': None,
                    'altura': None
                },
                {
                    'img': "wailord.gif",
                    'width': '150px',
                    'nome': 'Wailord',
                    'evolucao': None,
                    'peso': None,
                    'altura': None
                },
                {
                    'img': "mareep.gif",
                    'width': '150px',
                    'nome': 'Mareep',
                    'evolucao': 'Flaffly',
                    'peso': None,
                    'altura': None
                },
                {
                    'img': "flaffy.gif",
                    'width': '150px',
                    'nome': 'Flaffy',
                    'evolucao': 'Ampharos',
                    'peso': None,
                    'altura': None
                },
                {
                    'img': "ampharos.gif",
                    'width': '150px',
                    'nome': 'Ampharos',
                    'evolucao': None,
                    'peso': None,
                    'altura': None
                },
                {
                    'img': "aerodactyl.gif",
                    'width': '150px',
                    'nome': 'Aerodactyl',
                    'evolucao': None,
                    'peso': None,
                    'altura': None
                },
                {
                    'img': "lapras.gif",
                    'width': '150px',
                    'nome': 'Lapras',
                    'evolucao': None,
                    'peso': None,
                    'altura': None
                },
                {
                    'img': "latias.gif",
                    'width': '150px',
                    'nome': 'Latias',
                    'evolucao': None,
                    'peso': None,
                    'altura': None
                },
                {
                    'img': "latios.gif",
                    'width': '150px',
                    'nome': 'Latios',
                    'evolucao': None,
                    'peso': None,
                    'altura': None
                },
                {
                    'img': "teddiursa.gif",
                    'width': '150px',
                    'nome': 'Teddiursa',
                    'evolucao': 'Ursaring',
                    'peso': None,
                    'altura': None
                },
                {
                    'img': "ursaring.gif",
                    'width': '150px',
                    'nome': 'Ursaring',
                    'evolucao': None,
                    'peso': None,
                    'altura': None
                },
            ]

        def load(self, name):
            for pokemon in self.pokemons:
                if pokemon['nome'] == name:
                    return pokemon
            return None

        def sale(self):
            sales = []
            for x in self.loja:
                for y in self.pokemons:
                    if x['nome'] == y['nome']:
                        z = y
                        z.update(x)

                        sales.append(z)
                        break

            return sales

        def buy(self, price, poke, user):
            usuario.ListUsuario().money(price, user)
            self.saveDatabase(name=poke, user_id=user)

        def loadDatabasebyName(self, name, user_id):
            s = sessionmaker(bind=engine)()
            poke = []
            for x in list(s.query(Pokemon).filter(Pokemon.user_id.in_([user_id]), Pokemon.nome.in_([name]))):
                poke.append(ObjetoPokemon(x))

            return poke

        def loadDatabase(self, user_id):
            s = sessionmaker(bind=engine)()
            poke = []
            for x in list(s.query(Pokemon).filter(Pokemon.user_id.in_([user_id]))):
                poke.append(ObjetoPokemon(x))

            return poke

        def saveDatabase(self, name, user_id):
            s = sessionmaker(bind=engine)()
            pokemon = self.load(name)

            poke = s.query(Pokemon).filter(Pokemon.nome.in_([name]), Pokemon.user_id.in_([user_id])).first()

            if not poke:
                poke = Pokemon(img=pokemon['img'],
                               width=pokemon['width'],
                               nome=pokemon['nome'],
                               altura=pokemon['altura'],
                               peso=pokemon['peso'],
                               evolucao=pokemon['evolucao'],
                               user_id=user_id)
                s.add(poke)
                s.commit()



            return poke

    instance = None

    def __init__(self):
        if not ListPokemon.instance:
            ListPokemon.instance = ListPokemon.__ListPokemon()

    def __getattr__(self, item):
        return getattr(self.instance, item)
