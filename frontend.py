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
                if self.users[i].username == username:
                    return i
            return None

        def updateUser(self, username):
            index = self.getUserIndex(username)
            if index:
                self.users[index].time = datetime.now()

            else:
                self.users.append(type('obj', (object,), {'username': username, 'time': datetime.now()}))

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

                if value.tamagotchi.state == 'Morto':
                    return

                healthRate = 0.01
                hungerRate = 0.01
                happyRate = 0.01
                taxa = 1

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
                    healthRate = 0.02

                if value.tamagotchi.state == 'Faminto':
                    hungerRate = 0.02

                if value.tamagotchi.state == 'Triste':
                    happyRate = 0.02

                self.setTamagotchiHistory(value.tamagotchi.id,
                                          hunger=-1*taxa * hungerRate * deltaTime,
                                          happy=-1*happyRate * deltaTime * taxa,
                                          health=-1*healthRate * deltaTime * taxa)

                print('history', value.history)

                if 30 * 60 < int(deltaTime) < 60 * 60:
                    value.tamagotchi.name_pokemon = value.tamagotchi.name_pokemon[0:-1] + '2'

                elif 60 * 60 < int(deltaTime):
                    value.tamagotchi.name_pokemon = value.tamagotchi.name_pokemon[0:-1] + '3'

                self.SavePokemon(value.tamagotchi.name_pokemon, value.tamagotchi.user_id)

                self.SaveTamagotchi(id)

        def getDatabaseTamagotchi(self, id):
            s = sessionmaker(bind=engine)()
            return s, s.query(Tamagotchi).filter(Tamagotchi.id.in_([id])).first()

        def SaveTamagotchi(self,id):
            s, DataTamagotchi = self.getDatabaseTamagotchi(id)
            LocalTamagotchi = self.tamagotchis[self.getTamagotchiIndex(id)]

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
            poke = s.query(Pokemon).filter(
                    Pokemon.name.in_([name]),
                    Pokemon.user_id.in_([user_id])).first()
            if not poke:
                poke = Pokemon(name, user_id)
                s.add(poke)
                s.commit()
            return poke

        def DeleteTamagotchi(self, id):
            s = sessionmaker(bind=engine)()
            tama = s.query(Tamagotchi).filter(Tamagotchi.id.in_([int(id)])).first()
            s.delete(tama)
            s.commit()
            return True

        def getSessionUser(self):
            if 'username' in session:
                username = str(session.get('username'))
                self.updateUser(username)
                user = list(sessionmaker(bind=engine)().query(User).filter(User.username.in_([username])))
                if len(user):
                    return user[0]
            return None

        def MyTamagotchis(self, id=None, dead=False):
            user = self.getSessionUser()
            if id:
                tama = self.getTamagotchi(id=id, user_id=user.id, dead=dead)
            else:
                tama = self.getTamagotchi(user_id=user.id, dead=dead)

            if tama:
                return tama.tamagotchi

        def CreateUser(self, username, password):

            s = sessionmaker(bind=engine)()
            user = User(username, password)

            s.add(user)
            s.commit()

            self.SavePokemon(name='bul1', user_id=user.id)
            self.SavePokemon(name='char1', user_id=user.id)
            self.SavePokemon(name='sqr1', user_id=user.id)

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
            if name and user_id:
                return sessionmaker(bind=engine)().query(Pokemon).filter(Pokemon.name.in_([name]), Pokemon.user_id.in_([user_id]) ).first()
            elif name and not user_id:
                return sessionmaker(bind=engine)().query(Pokemon).filter(Pokemon.name.in_([name])).first()
            elif user_id and not name:
                return sessionmaker(bind=engine)().query(Pokemon).filter(Pokemon.user_id.in_([user_id]))
            else:
                return None

        def RedirectIndex(self):
            return redirect(url_for('.index'))

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
                self.games.append(type('obj', (object,), {'player1': player,
                                                          'player2': None,
                                                          'player1_piece': pieces[rand],
                                                          'player2_piece': pieces[0 if rand else 1],
                                                          'next': 'X',
                                                          'board': [
                                                              ['B', 'B', 'B'],
                                                              ['B', 'B', 'B'],
                                                              ['B', 'B', 'B']
                                                          ]}))
                return jsonify({'key': (len(self.games)-1), 'game': {'player1': self.games[len(self.games)-1].player1,
                                                                     'player2': self.games[len(self.games)-1].player2,
                                                                     'next': self.games[len(self.games)-1].next,
                                                                     'player1_piece': self.games[len(self.games)-1].player1_piece,
                                                                     'player2_piece': self.games[len(self.games)-1].player2_piece,
                                                                     'board': self.games[len(self.games)-1].board}})

            elif comand == 'Join':
                self.games[int(game)].player2 = player
                return jsonify({'key': int(game), 'game': {'player1': self.games[int(game)].player1,
                                                           'player2': self.games[int(game)].player2,
                                                           'next': self.games[int(game)].next,
                                                           'player1_piece': self.games[int(game)].player1_piece,
                                                           'player2_piece': self.games[int(game)].player2_piece,
                                                           'board': self.games[int(game)].board}})

            if comand == 'Wait':
                return jsonify({'key': int(game), 'game': {'player1': self.games[int(game)].player1,
                                                           'player2': self.games[int(game)].player2,
                                                           'next': self.games[int(game)].next,
                                                           'player1_piece': self.games[int(game)].player1_piece,
                                                           'player2_piece': self.games[int(game)].player2_piece,
                                                           'board': self.games[int(game)].board}})

            if comand == 'Move':
                linha = int(param[0])
                coluna = int(param[1])
                piece = self.games[int(game)].player1_piece
                next = self.games[int(game)].player2_piece
                if self.games[int(game)].player2 == player:
                    piece = self.games[int(game)].player2_piece
                    next = self.games[int(game)].player1_piece
                
                
                self.games[int(game)].next = next
                self.games[int(game)].board[linha][coluna] = piece


                return jsonify({'key': int(game), 'game': {'player1': self.games[int(game)].player1,
                                                           'player2': self.games[int(game)].player2,
                                                           'next': self.games[int(game)].next,
                                                           'player1_piece': self.games[int(game)].player1_piece,
                                                           'player2_piece': self.games[int(game)].player2_piece,
                                                           'board': self.games[int(game)].board}})

            if comand == 'Load':
                for x in len(self.games):
                    if self.games[x].player1 == player and self.games[x].player2:
                        return jsonify({'key': x, 'game': {'player1': self.games[x].player1,
                                                           'player2': self.games[x].player2,
                                                           'next': self.games[x].next,
                                                           'player1_piece': self.games[x].player1_piece,
                                                           'player2_piece': self.games[x].player2_piece,
                                                           'board': self.games[x].board}})
                    elif self.games[x].player2 == player and self.games[x].player1:
                        return jsonify({'key': x, 'game': {'player1': self.games[x].player1,
                                                           'player2': self.games[x].player2,
                                                           'next': self.games[x].next,
                                                           'player1_piece': self.games[x].player1_piece,
                                                           'player2_piece': self.games[x].player2_piece,
                                                           'board': self.games[x].board}})
                return jsonify({'error': 'Não ha games'})
            if comand == 'All':
                return jsonify({'games': map(lambda (i,x): {'player1': x.player1,
                                                            'key': i,
                                                            'player2': x.player2
                                                           }, enumerate(self.games))})

    instance = None

    def __init__(self):
        if not ConnectDatabase.instance:
            ConnectDatabase.instance = ConnectDatabase.__ConnectDatabase()

    def __getattr__(self, name):
        return getattr(self.instance, name)



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

            # Carregar Pokemon
            pokemon = DB.getPokemon(tamagotchi.name_pokemon, user.id)

            return jsonify( 
                {
                    'name': tamagotchi.name,
                    'happy': tamagotchi.happy,
                    'hunger': tamagotchi.hunger,
                    'health': tamagotchi.health,
                    'pokemon':
                        {
                            'name': pokemon.name,
                            'cenario': pokemon.cenario
                        },
                    'age': (tamagotchi.last_update - tamagotchi.birthday).total_seconds(),
                    'list': map(lambda tama: (
                        {
                            'id': tama.id,
                            'name': tama.name,
                            'state': tama.state,
                            'pokemon': tama.name_pokemon
                        }), tamagotchis)
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
    DB.initTamagotchis()
    if id:
        user = DB.getSessionUser()
        if user:
            return render_template('index.html',
                                   tamagotchis=DB.AllTamagotchis(user_id=user.id),
                                   tamagotchi=DB.MyTamagotchis(int(id)))
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
            str(request.form['password'])
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
    IMAGEM = str(request.form['poke'])

    DB.SavePokemon(name=IMAGEM, user_id=user.id)
