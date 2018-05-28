# -*- coding: utf-8 -*-
from flask import flash, url_for, request, session, redirect, jsonify

from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///tutorial.db', echo=True)

from flask import Blueprint, render_template
from flask_nav.elements import Navbar, View
from nav import nav
from datetime import datetime
from random import randint

frontend = Blueprint('frontend', __name__)

# navbar logado
nav.register_element('frontend_top', Navbar(
    View('Tamagotchi', '.index'),
    View('Deslogar', '.logout'),
    View('Criar Tamagotchi', '.novotamagotchi'),
    View('Ranking', '.rank'),
    ))

# navbar Deslogado
nav.register_element('no_login', Navbar(
    View('Tamagotchi', '.index'),
    View('Ranking', '.rank'),
    ))


class ConnectDatabase:
    class __ConnectDatabase:
        # Singleton Constructor Python
        def __init__(self):
            self.tamagotchis = []
            self.users = []
            self.games = []
            self.taxa = 1
            self.loja = [
                {'nome': 'Lugia', 'price': 500.0},
                {'nome': 'Mewtwo', 'price': 700.0},
                {'nome': 'Onix', 'price': 100.0},
                {'nome': 'Pichu', 'price': 100.0},
                {'nome': 'Munchlax', 'price': 100.0}
            ]
            self.pokemons = [
                {
                    'img':"Bulbasaur.gif", 
                    'width':'120px',
                    'nome': 'Bulbasaur',
                    'time': 30*60,
                    'evolucao':'Ivysaur',
                    'peso': '6.9 Kg', 
                    'altura':'0.7 m' 
                },
                {
                    'img':"ivysaur.gif", 
                    'width':'150px',
                    'nome': 'Ivysaur',
                    'time': 60*60,
                    'evolucao':'Venusaur',
                    'peso': '13.0 Kg', 
                    'altura':'1.0 m' 
                },
                {
                    'img': "venusaur.gif", 
                    'width': '200px',
                    'nome': 'Venusaur',
                    'evolucao': None,
                    'peso': '100.0 Kg', 
                    'altura':'2.0 m' 
                },
                {
                    'img': "charmander.gif", 
                    'width': '130px',
                    'nome': 'Charmander',
                    'time': 30*60,
                    'evolucao': 'Charmeleon',
                    'peso': '8.5 Kg', 
                    'altura':'0.6 m' 
                },
                {
                    'img': "charmeleon.gif", 
                    'width': '150px',
                    'nome': 'Charmeleon',
                    'time': 60*60,
                    'evolucao': 'Charizard',
                    'peso': '19.0 Kg', 
                    'altura':'1.1 m' 
                },
                {
                    'img': "charizard.gif", 
                    'width': '200px',
                    'nome': 'Charizard',
                    'evolucao': None,
                    'peso': '90.5 Kg', 
                    'altura':'1.7 m' 
                },
                {
                    'img': "squirtle.gif", 
                    'width': '130px',
                    'nome': 'Squirtle',
                    'time': 30*60,
                    'evolucao': 'Wartortle',
                    'peso': '9.0 Kg', 
                    'altura':'0.5 m' 
                },
                {
                    'img': "wartortle.gif", 
                    'width': '150px',
                    'nome': 'Wartortle',
                    'time': 60*60,
                    'evolucao': 'Blastoise',
                    'peso': '22.5 Kg', 
                    'altura':'1.0 m' 
                },
                {
                    'img': "blastoise-mega.gif", 
                    'width': '170px',
                    'nome': 'Blastoise',
                    'evolucao': None,
                    'peso': '85.5 Kg', 
                    'altura':'1.6 m' 
                },
                {
                    'img': "blastoise-mega.gif",
                    'width': '170px',
                    'nome': 'Blastoise',
                    'evolucao': None,
                    'peso': '85.5 Kg',
                    'altura':'1.6 m'
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
                }
            ]

        def GetSalePokemons(self):
            sales = []
            for x in self.loja:
                for y in self.pokemons:
                    if x['nome'] == y['nome']:
                        z = y
                        z.update(x)

                        sales.append(z)
                        break

            return sales


        def GetPokemonFile(self, name):
            for pokemon in self.pokemons:
                if pokemon['nome'] == name:
                    return pokemon
            return None

        def initTamagotchis(self):
            self.prepareTamagotchi()
            for x in self.tamagotchis:
                self.engineTamagotchi(x.tamagotchi.id)
                self.SaveTamagotchi(x.tamagotchi.id)

            self.tamagotchis = []

            for i in sessionmaker(bind=engine)().query(Tamagotchi).all():
                self.tamagotchis.append(type('obj', (object,), {'tamagotchi': i, 'history': []}))

        def prepareTamagotchi(self):
            for x in range(len(self.tamagotchis)):
                health = self.tamagotchis[x].tamagotchi.health
                hunger = self.tamagotchis[x].tamagotchi.hunger
                happy = self.tamagotchis[x].tamagotchi.happy
                for y in range(len(self.tamagotchis[x].history)):
                    health = health + self.tamagotchis[x].history[y].health
                    hunger = hunger + self.tamagotchis[x].history[y].hunger
                    happy = happy + self.tamagotchis[x].history[y].happy
                self.tamagotchis[x].tamagotchi.health = health
                self.tamagotchis[x].tamagotchi.happy = happy
                self.tamagotchis[x].tamagotchi.hunger = hunger

        def getTamagotchiIndex(self, id=None, user_id=None, dead=False):
            condition_dead = True
            condition_id = True
            condition_user_id = True
            for i in range(len(self.tamagotchis)):
                if id:
                    condition_id = self.tamagotchis[i].tamagotchi.id == id
                if user_id:
                    condition_user_id = self.tamagotchis[i].tamagotchi.user_id == user_id

                if dead:
                    condition_dead = self.tamagotchis[i].tamagotchi.state != 'Dead'

                if condition_user_id and condition_dead and condition_id:
                    return i
            return None

        def getUserIndex(self, username):
            for i in range(len(self.users)):
                if self.users[i].user.username == username:
                    return i
            return None

        def updateUser(self, user):
            index = self.getUserIndex(user.username)
            if isinstance(index, int):
                self.users[index].time = datetime.now()

            else:
                self.users.append(type('obj', (object,), {'user': user, 'time': datetime.now()}))

        def setTamagotchiHistory(self, id=None, health=0.0, happy=0.0, hunger=0.0):
            index = self.getTamagotchiIndex(id=id)
            if isinstance(index, int):
                self.tamagotchis[index].history.append(type('obj', (object,), {'health': health, 'hunger': hunger, 'happy': happy}))
                return self.tamagotchis[index].history
            else:
                self.initTamagotchis()
                self.setTamagotchiHistory(id, health, happy, hunger)

        def getTamagotchi(self, id=None, user_id=None, dead=False):
            index = self.getTamagotchiIndex(id=id, user_id=user_id, dead=dead)
            if isinstance(index, int):
                return self.tamagotchis[index]
            else:
                return None

        def engineTamagotchi(self, id=None):
            if id:
                value = self.getTamagotchi(id)
                if not value:
                    return
                if value.tamagotchi.state == 'Morto':
                    return

                healthRate = 0.001
                hungerRate = 0.001
                happyRate = 0.001
                taxa = self.taxa

                deltaTime = (datetime.now() - value.tamagotchi.last_update).total_seconds()

                if value.tamagotchi.happy <= 0 or value.tamagotchi.health <= 0 or value.tamagotchi.hunger <= 0:
                    value.tamagotchi.state = 'Morto'

                # atualiza estados
                elif value.tamagotchi.happy < 50:
                    value.tamagotchi.state = 'Triste'

                elif value.tamagotchi.health < 60:
                    value.tamagotchi.state = 'Doente'

                elif value.tamagotchi.hunger < 60:
                    value.tamagotchi.state = 'Faminto'

                if value.tamagotchi.state == 'Doente':
                    healthRate = 0.002

                if value.tamagotchi.state == 'Faminto':
                    hungerRate = 0.002

                if value.tamagotchi.state == 'Triste':
                    happyRate = 0.002

                self.setTamagotchiHistory(value.tamagotchi.id,
                                          hunger=-1*taxa * hungerRate * deltaTime,
                                          happy=-1*happyRate * deltaTime * taxa,
                                          health=-1*healthRate * deltaTime * taxa)

                print('history', value.history)

                mypoke = self.GetPokemonFile(value.tamagotchi.name_pokemon)
                if mypoke['evolucao']:
                    if mypoke['time'] < (datetime.now() - value.tamagotchi.birthday).total_seconds():
                        self.SavePokemon(mypoke['evolucao'], value.tamagotchi.user_id)
                        value.tamagotchi.name_pokemon = mypoke['evolucao']

                self.SaveTamagotchi(id)

        def getOnlineUser(self):
            user = []
            for x in self.users:
                if (datetime.now() - x.time).total_seconds() < 5*60:
                    user.append(x)
            return user

        def getDatabaseTamagotchi(self, id):
            s = sessionmaker(bind=engine)()
            return s, s.query(Tamagotchi).filter(Tamagotchi.id.in_([id])).first()

        def SaveTamagotchi(self,id):
            s, DataTamagotchi = self.getDatabaseTamagotchi(id)
            index = self.getTamagotchiIndex(id)
            if not isinstance(index, int):
                return

            LocalTamagotchi = self.tamagotchis[index]

            if DataTamagotchi.state == 'Morto':
                return

            DataTamagotchi.health = DataTamagotchi.health + sum([x.health for x in LocalTamagotchi.history])
            DataTamagotchi.hunger = DataTamagotchi.hunger + sum([x.hunger for x in LocalTamagotchi.history])
            DataTamagotchi.happy = DataTamagotchi.happy + sum([x.happy for x in LocalTamagotchi.history])

            if DataTamagotchi.health < 0:
                DataTamagotchi.health = 0

            elif 100 < DataTamagotchi.health:
                DataTamagotchi.health = 100

            if DataTamagotchi.happy < 0:
                DataTamagotchi.happy = 0

            elif 100 < DataTamagotchi.happy:
                DataTamagotchi.happy = 100

            if DataTamagotchi.hunger < 0:
                DataTamagotchi.hunger = 0

            elif 100 < DataTamagotchi.hunger:
                DataTamagotchi.hunger = 100

            DataTamagotchi.name_pokemon = LocalTamagotchi.tamagotchi.name_pokemon
            DataTamagotchi.state = LocalTamagotchi.tamagotchi.state

            DataTamagotchi.last_update = datetime.now()

            s.commit()

        def SavePokemon(self, name, user_id):
            s = sessionmaker(bind=engine)()
            print(name)
            pokemon = self.GetPokemonFile(name)

            poke = s.query(Pokemon).filter(
                    Pokemon.nome.in_([name]),
                    Pokemon.user_id.in_([user_id])).first()
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

        def DeleteTamagotchi(self, id):
            s = sessionmaker(bind=engine)()
            tama = s.query(Tamagotchi).filter(Tamagotchi.id.in_([int(id)])).first()
            index= self.getTamagotchiIndex(id=id)
            del self.tamagotchis[index]
            s.delete(tama)
            s.commit()
            return True

        def getSessionUser(self):
            if 'username' in session:
                username = str(session.get('username'))
                user = list(sessionmaker(bind=engine)().query(User).filter(User.username.in_([username])))[0]
                self.updateUser(user)
                if user:
                    return user
            return None

        def MyTamagotchis(self, id=None, dead=False):
            user = self.getSessionUser()
            if id:
                tama = self.getTamagotchi(id=id, user_id=user.id, dead=dead)
            else:
                tama = self.getTamagotchi(user_id=user.id, dead=dead)

            if tama:
                return tama.tamagotchi

        def CreateUser(self, username, password, imagem):

            s = sessionmaker(bind=engine)()
            user = User(username, password, imagem)

            s.add(user)
            s.commit()

            self.SavePokemon(name='Bulbasaur', user_id=user.id)
            self.SavePokemon(name='Charmander', user_id=user.id)
            self.SavePokemon(name='Squirtle', user_id=user.id)

            return user

        def CreateTamagotchi(self, name, user_id, imagem):
            s = sessionmaker(bind=engine)()
            tamago = Tamagotchi(
                name=name,
                user_id=user_id,
                imagem=imagem)

            s.add(tamago)
            s.commit()

            return tamago

        def AllTamagotchis(self, user_id=None):
            self.initTamagotchis()
            todos = [x.tamagotchi for x in self.tamagotchis]
            if user_id:
                todos = [x.tamagotchi for x in filter(lambda y: y.tamagotchi.user_id == user_id, self.tamagotchis)]
            return sorted(todos, key=lambda tama: (tama.last_update - tama.birthday).total_seconds(), reverse=True)

        def getPokemon(self, name=None, user_id=None):
            pokemons = []
            if name and user_id:
                pokemons = list(sessionmaker(bind=engine)().query(Pokemon).filter(Pokemon.nome.in_([name]), Pokemon.user_id.in_([user_id]) ))
            else:
                pokemons = list(sessionmaker(bind=engine)().query(Pokemon).filter(Pokemon.user_id.in_([user_id])) )
            
            return[{
                    'id': pokemon.id,
                    'nome': pokemon.nome,
                    'img': pokemon.img,
                    'width': pokemon.width,
                    'altura': pokemon.altura,
                    'peso': pokemon.peso,
                    'evolucao': pokemon.evolucao,
                    'cenario': pokemon.cenario,
                    'user': self.getUser(pokemon.user_id) 
                } for pokemon in pokemons]


        def getUser(self,id):
            session = sessionmaker(bind=engine)()
            user = session.query(User).filter(User.id.in_([id])).first()
            
            return {
                'id': user.id,
                'money': user.money,
                'username': user.username
            }
        def RedirectIndex(self):
            return redirect(url_for('.index'))

        def UserReward(self, size, username):
            session = sessionmaker(bind=engine)()

            user = session.query(User).filter(User.username.in_([username])).first()
            user.money = user.money + size
            session.commit()


        def Login(self, username=None, password=None):
            if username and password:
                user = sessionmaker(bind=engine)().query(User).filter(
                    User.username.in_([username]),
                    User.password.in_([password])
                )

                if user:
                    session['logged_in'] = True
                    session['username'] = username
                    return True

            return False

        def Logout(self):
            session.pop('username', None)
            session.pop('logged_in', None)
            return True

        def GetUserByTamagotchi(self,id):
            return list(sessionmaker(bind=engine)().query(User).filter(User.id.in_([id])))

        def AjaxResponse(self, name, mensagem):
            return jsonify({name: mensagem})

        def Jogo_Da_Velha(self, comand=None, game=None, param=None, player=None):

            if not comand:
                return None

            if not self.games:
                self.games = []

            if comand == 'New':

                pieces = ['X', 'O']
                rand = randint(0, 1)
                key = len(self.games)
                self.games.append(Jogo_da_Velha(player1=player,
                                                key=key,
                                                player1_piece=pieces[rand],
                                                player2_piece=pieces[0 if rand else 1]))

                return jsonify({'key': key,
                                'game': self.games[key].get()})

            elif comand == 'Join':
                self.games[int(game)].Join(player)
                key = int(game)
                return jsonify({'key': key,
                                'game': self.games[key].get()})

            if comand == 'Wait':
                key = int(game)
                return jsonify({'key': key,
                                'game': self.games[key].get()})

            if comand == 'Move':
                self.games[int(game)].Movement(player=player,
                                               casa=param)
                key = int(game)
                return jsonify({'key': key,
                                'game': self.games[key].get()})

            if comand == 'All':
                return jsonify({'games': map(lambda x: x.get(), self.games)})

    instance = None

    def __init__(self):
        if not ConnectDatabase.instance:
            ConnectDatabase.instance = ConnectDatabase.__ConnectDatabase()

    def __getattr__(self, name):
        return getattr(self.instance, name)


class Jogo_da_Velha():

    def __init__(self, player1=None, player2=None, key=None, player1_piece=None, player2_piece=None):
        self.player1 = player1
        self.player2 = player2
        self.key = key
        self.next_piece = 'X'
        self.player1_piece = player1_piece
        self.player2_piece = player2_piece
        self.board = [['B', 'B', 'B'],
                      ['B', 'B', 'B'],
                      ['B', 'B', 'B']]
        self.state = 'Game Started'
        self.last_action = datetime.now()

    def Join(self, player):
        p = 0
        self.last_action = datetime.now()
        if self.player1 == player:
            p = 1
        elif self.player2 == player:
            p = 2
        elif not self.player1:
            self.player1 = player
            p = 1
        elif not self.player2:
            self.player2 = player
            p = 2
        return p

    def Movement(self, player, casa):
        self.last_action = datetime.now()
        self.board[int(casa[0])][int(casa[1])] = self.player2_piece if self.player2 == player else self.player1_piece
        self.next_piece = self.player2_piece if self.player1 == player else self.player1_piece

    def get(self):
        return {'player1': self.player1,
                'player2': self.player2,
                'next': self.next_piece,
                'player1_piece': self.player1_piece,
                'player2_piece': self.player2_piece,
                'board': self.board,
                'key': self.key,
                'idle': int((datetime.now()-self.last_action).total_seconds())
                }


@frontend.route('/load', methods=['POST'])
def load_tamagotchi():
    DB = ConnectDatabase()
    DB.initTamagotchis()
    # Pega id do tamagotchi pego por requisicao ajax
    id = request.form['id']
    if not id:
        return DB.AjaxResponse('error', 'parametro <'+id+'> não encontrado')
    # Carregar Usuario logado
    user = DB.getSessionUser()
    if user:
        # Carregar meus tamagotchis
        tamagotchis = DB.AllTamagotchis(user_id=user.id)

        # Pega Tamagotchi pelo id
        tamagotchi = DB.MyTamagotchis(id=int(id))
        if tamagotchi:

            return jsonify( 
                {
                    'name': tamagotchi.name,
                    'happy': tamagotchi.happy,
                    'hunger': tamagotchi.hunger,
                    'health': tamagotchi.health,
                    'money': user.money,
                    'pokemon': DB.getPokemon(tamagotchi.name_pokemon, user.id)[0],
                    'age': (tamagotchi.last_update - tamagotchi.birthday).total_seconds(),
                    'list': map(lambda tama: (
                        {
                            'id': tama.id,
                            'name': tama.name,
                            'state': tama.state,
                            'pokemon': DB.getPokemon(tama.name_pokemon, tama.user_id)[0]
                        }), tamagotchis )
                })
        else:
            return DB.AjaxResponse('error', 'Tamagotchi nao encontrado ou falha no banco')
    else:
        return DB.AjaxResponse('error', 'Sessao expirada')


@frontend.route('/tamagotchiform')
def novotamagotchi():
    DB = ConnectDatabase()
    user = DB.getSessionUser()
    if user:
        pokemons = DB.getPokemon(user_id=user.id)
        return render_template('tamagotchi_form.html', pokemons=pokemons)
    else:
        return redirect(url_for('.index'))


@frontend.route('/')
def index():
    DB = ConnectDatabase()
    user = DB.getSessionUser()
    if not user:
        return render_template('login.html')
    else:
        DB.initTamagotchis()
        tama = DB.MyTamagotchis(dead=True)
        if tama:
            return redirect(url_for('.home', id=tama.id))
        else:
            return redirect(url_for('.home'))

@frontend.route('/reward', methods=['POST'])
def Reward():
    DB = ConnectDatabase()
    player1 = str(request.form['player1'])
    player2 = str(request.form['player2'])
    DB.UserReward(int(request.form['reward']), player1)
    if player2:
        DB.UserReward(int(request.form['reward']), player2)
        
    return jsonify({'success': 'usuario recebeu sua recompensa!'})

@frontend.route('/tamagotchi/update/health', methods=['POST'])
def health():
    DB = ConnectDatabase()
    if request.method == 'POST':
        value = DB.setTamagotchiHistory(id=int(request.form['id'], 10), health=int(request.form['value'], 10))
        return DB.AjaxResponse('success', value)
    else:
        DB.setTamagotchiHistory(id=int(id, 10), happy=int(value, 10))
        return redirect(url_for('.home', id=id))


@frontend.route('/tamagotchi/update/hunger', methods=['POST'])
def hunger(id=None, value=20):
    DB = ConnectDatabase()
    if request.method == 'POST':
        value = DB.setTamagotchiHistory(id=int(request.form['id'], 10), hunger=int(request.form['value'], 10))
        return DB.AjaxResponse('success', value)
    else:
        DB.setTamagotchiHistory(id=int(id, 10), hunger=int(value, 10))
        return redirect(url_for('.home', id=id))


@frontend.route('/tamagotchi/update/happy', methods=['POST'])
def happy(id=None, value=20):
    DB = ConnectDatabase()
    if request.method == 'POST':
        value = DB.setTamagotchiHistory(id=int(request.form['id'], 10), happy=int(request.form['value'], 10))
        return DB.AjaxResponse('success', {'success': value})
    else:
        DB.setTamagotchiHistory(id=int(id, 10), happy=int(value, 10))
        return redirect(url_for('.home', id=id))


@frontend.route('/games/jogo_da_velha', methods=['POST'])
def games():
    DB = ConnectDatabase()
    user = DB.getSessionUser()
    if user:
        if str(request.form['game_name']) == 'Jogo_da_Velha':
            return DB.Jogo_Da_Velha(comand=str(request.form['comand']),
                                    game=request.form['game'],
                                    param=str(request.form['param']),
                                    player=user.username)
    return jsonify({'error': 'Algo de errado aconteceu'})

@frontend.route('/tamagotchi')
@frontend.route('/tamagotchi/<id>')
def home(id=None):
    DB = ConnectDatabase()
    if id:
        user = DB.getSessionUser()
        pokemons = DB.GetSalePokemons()

       
        if user:
            return render_template('index.html',
                                   tamagotchis=DB.AllTamagotchis(user_id=user.id),
                                   tamagotchi=DB.MyTamagotchis(int(id)),
                                   pokemons=pokemons, logados = DB.getOnlineUser())
        else:
            return DB.RedirectIndex()
    else:
        return render_template('welcome.html')


@frontend.route('/cadastrar', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('user_form.html')
    elif request.method == 'POST':

        DB = ConnectDatabase()
        DB.CreateUser(
            str(request.form['username']),
            str(request.form['password']),
            str(request.form['persona']),
        )

        return DB.RedirectIndex()


@frontend.route('/login', methods=['POST'])
def do_login():
    DB = ConnectDatabase()

    if not DB.Login(
                        username=str(request.form['username']),
                        password=str(request.form['password'])
                        ):
        flash("Login ou senha incorreta")
    return DB.RedirectIndex()
 
@frontend.route("/logout")
def logout():
    DB = ConnectDatabase()
    DB.Logout()
    return DB.RedirectIndex()

@frontend.route('/novotamagotchi', methods=['POST'])
def do_novo_tamagotchi():
    POST_NOME = str(request.form['nome'])
    IMAGEM = str(request.form['poke'])
    if POST_NOME == '':
        flash("De um nome ao Tamagotchi")
        return redirect(url_for('.novotamagotchi'))
    
    if IMAGEM == '':
        flash("Escolha um Tamagotchi")
        return redirect(url_for('.novotamagotchi'))

    if verificaNome(POST_NOME):
        flash("Ja existe um tamagotchi com este nome")
        return redirect(url_for('.novotamagotchi'))
    else:

        DB = ConnectDatabase()
        user = DB.getSessionUser()
        DB.CreateTamagotchi(
            name=POST_NOME,
            user_id=user.id,
            imagem=IMAGEM)

        return DB.RedirectIndex()

@frontend.route('/user/get', methods=['POST'])
def getUser():
    DB = ConnectDatabase()
    user = DB.getSessionUser()
    return jsonify({'user': user.username})

@frontend.route('/ranking')
def rank():
    DB = ConnectDatabase()
    return render_template('rank.html',
                           tamagotchis=DB.AllTamagotchis(),
                           pegaCriadorDoTamagotchi=DB.GetUserByTamagotchi)

def verificaNome(nome):
    s = sessionmaker(bind=engine)()

    teste = s.query(Tamagotchi).filter(Tamagotchi.name.in_([nome])).first()

    if teste:
        return True
    else:
        return False

@frontend.route('/tamagotchi/del', methods=['POST'])
def deletaBixo():
    DB = ConnectDatabase()
    DB.DeleteTamagotchi(request.form['id'])

    return DB.RedirectIndex()

@frontend.route('/tamagotchi/buy', methods=['POST'])
def compraBixo():
    DB = ConnectDatabase()

    user = DB.getSessionUser()

    PRICE = float(request.form['price'])
    IMAGEM = str(request.form['poke'])

    if user.money > PRICE:
        DB.SavePokemon(name=IMAGEM, user_id=user.id)
    else:
        flash("Voce so tem $ "+str(user.money)+" falta $ "+str(PRICE - user.money)+". Continue tentando")
    return DB.RedirectIndex()
