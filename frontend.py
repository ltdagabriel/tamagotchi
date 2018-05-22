# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

from flask import flash, url_for, request, session, redirect, jsonify

from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///tutorial.db', echo=True)

from flask import Blueprint, render_template
from flask_nav.elements import Navbar, View
from nav import nav
from datetime import datetime

frontend = Blueprint('frontend', __name__)




# We're adding a navbar as well through flask-navbar. In our example, the
# navbar has an usual amount of Link-Elements, more commonly you will have a
# lot more View instances.

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


class ConnectDatabase():
    # Session
    s = None
    # Tamagotchi Local List
    tamagotchis = []
    # Usuarios que acessaram o sistema
    users = []
    # Factory Constructor
    connect = None

    def getFactory(self):
        if not self.connect:
            self.s = sessionmaker(bind=engine)
            self.connect = ConnectDatabase()
        return self.connect

    def initTamagotchis(self):
        for x in self.tamagotchis:
            self.SaveTamagotchi(x.tamagotchi.id)

        for i in self.s.query(Tamagotchi).all():
            self.tamagotchis.append(type('obj', (object,), {'tamagotchi' : i, 'history': []}))
    
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
            self.tamagotchis[x].history = []

    def getTamagotchiIndex(self, id=None, user_id=None, dead=True):
        condition_dead = True
        condition_id = True
        condition_user_id = True
        for i in range(len(self.tamagotchis)):
            if not dead:
                condition_dead = self.tamagotchis[i].tamagotchi.state != 'Dead'
            if id:
                condition_id = self.tamagotchis[i].tamagotchi.id == id
            if user_id:
                condition_user_id = self.tamagotchis[i].tamagotchi.user_id == user_id

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

    def setTamagotchiHistory(self, id=None, health=0, happy=0, hunger=0):
        if id:
            index = self.getTamagotchiIndex(id)

            self.tamagotchis[index].history.append(type('obj', (object,), {'health': health, 'happy': happy, 'hunger': hunger }))
        else:
            return None

    def getTamagotchi(self, id=None, user_id=None, dead=True):
        return self.tamagotchis[self.getTamagotchiIndex(id=id, user_id=user_id, dead=dead)]

    def engineTamagotchi(self, id=None):
        if id:
            value = self.getTamagotchi(id)
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

            self.setTamagotchiHistory(id,
                                      hunger=taxa * hungerRate * deltaTime,
                                      happy=happyRate * deltaTime * taxa,
                                      health=healthRate * deltaTime * taxa)

            if 30 * 60 < int(deltaTime) < 60 * 60:
                value.tamagotchi.name_pokemon = value.tamagotchi.name_pokemon[0:-1] + '2'

            elif 60 * 60 < int(deltaTime):
                value.tamagotchi.name_pokemon = value.tamagotchi.name_pokemon[0:-1] + '3'
            self.SavePokemon(value.tamagotchi.name_pokemon, value.tamagotchi.user_id)

            self.SaveTamagotchi(id)

    def getDatabaseTamagotchi(self, id):
        return self.s.query(Tamagotchi).filter(Tamagotchi.id.in_([id])).first()

    def SaveTamagotchi(self,id):
        DataTamagotchi = self.getDatabaseTamagotchi(id)
        LocalTamagotchi = self.tamagotchis[self.getTamagotchiIndex(id)]

        DataTamagotchi.health = sum([x.health for x in LocalTamagotchi.history])
        DataTamagotchi.hunger = sum([x.hunger for x in LocalTamagotchi.history])
        DataTamagotchi.happy = sum([x.happy for x in LocalTamagotchi.history])

        DataTamagotchi.name_pokemon = LocalTamagotchi.tamagotchi.name_pokemon
        DataTamagotchi.state = LocalTamagotchi.tamagotchi.state

        DataTamagotchi.last_update = datetime.now()

        self.s.commit()

    def SavePokemon(self, name, user_id):
        poke = self.s.query(Pokemon).filter(
                Pokemon.name.in_([name]),
                Pokemon.user_id.in_([user_id])).first()
        if not poke:
            poke = Pokemon(name, user_id)
            self.s.add(poke)
        return poke

    def DeleteTamagotchi(self, id):
        tama = self.s.query(Tamagotchi).filter(Tamagotchi.id.in_([int(id)])).first()
        self.s.delete(tama)
        self.s.commit()
        return True

    def getSessionUser(self):
        if 'username' in session:
            username = str(session.get('username'))
            self.updateUser(username)
            return self.s.query(User).filter(User.username.in_([username])).first()
        return None

    def MyTamagotchis(self, id=None):
        self.initTamagotchis()
        user = self.getSessionUser()
        tama = None
        if id:
            if user:
                tama = self.getTamagotchi(id, user.id)
            else:
                tama = self.getTamagotchi(id)

            if tama:
                return tama.tamagotchi
        else:
            if user:
                return self.getTamagotchi(user_id=user.id, dead=False)
            else:
                return None

    def CreateUser(self, username, password):

        user = User(username, password)

        self.s.add(user)
        self.s.commit()

        self.SavePokemon(name='bull', user_id=user.id)
        self.SavePokemon(name='charl', user_id=user.id)
        self.SavePokemon(name='sqrl', user_id=user.id)

        return user

    def CreateTamagotchi(self, name, user_id, imagem):

        tamago = Tamagotchi(
            name=name,
            user_id=user_id,
            imagem=imagem)

        self.s.add(tamago)
        self.s.commit()

        return tamago

    def AllTamagotchis(self, user_id=None):
        self.initTamagotchis()
        todos = [x.tamagotchi for x in self.tamagotchis]
        if user_id:
            todos = [x.tamagotchi for x in filter(lambda y: y.tamagotchi.user_id == user_id, self.tamagotchis)]
        return sorted(todos, key=lambda tama: (tama.last_update - tama.birthday).total_seconds(), reverse=True)

    def getPokemon(self, name=None, user_id=None):
        if name and user_id:
            return self.s.query(Pokemon).filter(Pokemon.name.in_([name]), Pokemon.user_id.in_([user_id]) ).first()
        elif name and not user_id:
            return self.s.query(Pokemon).filter(Pokemon.name.in_([name])).first()
        elif user_id and not name:
            return self.s.query(Pokemon).filter(Pokemon.user_id.in_([user_id]))
        else:
            return None

    def RedirectIndex(self):
        return redirect(url_for('.index'))

    def Login(self, username=None, password=None):
        if username and password:
            user = self.s.query(User).filter(User.username.in_([username]), User.password.in_([password]))
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
        return self.s.query(User).filter(User.id.in_([id])).first()

    def AjaxResponse(self, name, mensagem):
        return jsonify({name: mensagem})

@frontend.route('/load', methods=['POST'])
def load_tamagotchi():
    DB = ConnectDatabase.getFactory()

    # Pega id do tamagotchi pego por requisicao ajax
    id = request.form['id']
    if not id:
        return None
    # Carregar Usuario logado
    user = DB.getSessionUser()
    if user:
        # Carregar meus tamagotchis
        tamagotchis = DB.AllTamagotchis(user_id=user.id)

        # Pega Tamagotchi pelo id
        tamagotchi = DB.MyTamagotchis(id=int(id, 10))
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
            return DB.AjaxResponse('error', 'Tamagotchi não encontrado ou falha no banco')
    else:
        return DB.AjaxResponse('error', 'Sessao expirada')


@frontend.route('/tamagotchiform')
def novotamagotchi():
    DB = ConnectDatabase.getFactory()
    user = DB.getSessionUser()
    if user:
        pokemons = DB.getPokemon(user_id=user.id)
        return render_template('tamagotchi_form.html', pokemons=pokemons)
    else:
        return redirect(url_for('.index'))


@frontend.route('/')
def index():
    DB = ConnectDatabase.getFactory()
    user = DB.getSessionUser()
    if not user:
        return render_template('login.html')
    else:
        tama = DB.MyTamagotchis()
        if tama:
            return redirect(url_for('.home', id=tama.id))
        else:
            return redirect(url_for('.home'))


@frontend.route('/tamagotchi/health', methods=['POST'])
@frontend.route('/tamagotchi/<id>/health')
@frontend.route('/tamagotchi/<id>/health/<value>')
def health(id=None, value=20):
    DB = ConnectDatabase.getFactory()
    if request.method == 'POST':
        DB.setTamagotchiHistory(id=int(request.form['id'], 10), health=int(request.form['value'], 10))
        return DB.AjaxResponse('success', 'Vida atualizada')
    else:
        DB.setTamagotchiHistory(id=int(id, 10), health=int(value, 10))
        return redirect(url_for('.home', id=id))


@frontend.route('/tamagotchi/hunger', methods=['POST'])
@frontend.route('/tamagotchi/<id>/hunger')
@frontend.route('/tamagotchi/<id>/hunger/<value>')
def hunger(id=None, value=20):
    DB = ConnectDatabase.getFactory()
    if request.method == 'POST':
        DB.setTamagotchiHistory(id=int(request.form['id'], 10), hunger=int(request.form['value'], 10))
        return DB.AjaxResponse('success', 'Fome atualizada')
    else:
        DB.setTamagotchiHistory(id=int(id, 10), hunger=int(value, 10))
        return redirect(url_for('.home', id=id))


@frontend.route('/tamagotchi/happy', methods=['POST'])
@frontend.route('/tamagotchi/<id>/happy')
@frontend.route('/tamagotchi/<id>/happy/<value>')
def happy(id=None, value=20):
    DB = ConnectDatabase.getFactory()
    if request.method == 'POST':
        DB.setTamagotchiHistory(id=int(request.form['id'], 10), happy=int(request.form['value'], 10))
        return DB.AjaxResponse('success', 'Felicidade atualizada')
    else:
        DB.setTamagotchiHistory(id=int(id, 10), happy=int(value, 10))
        return redirect(url_for('.home', id=id))


@frontend.route('/tamagotchi')
@frontend.route('/tamagotchi/<id>')
def home(id=None):
    DB = ConnectDatabase.getFactory()
    if id:
        user = DB.getSessionUser()
        if user:
            return render_template('index.html',
                                   tamagotchis=DB.AllTamagotchis(user_id=user.id),
                                   tamagotchi=DB.MyTamagotchis(id))
        else:
            return DB.RedirectIndex()
    else:
        return render_template('welcome.html')


@frontend.route('/cadastrar', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('user_form.html')
    elif request.method == 'POST':

        DB = ConnectDatabase.getFactory()
        DB.CreateUser(
            str(request.form['username']),
            str(request.form['password'])
        )

        return DB.RedirectIndex()


@frontend.route('/login', methods=['POST'])
def do_login():
    DB = ConnectDatabase.getFactory()

    if not DB.Login(
                        username=str(request.form['username']),
                        password=str(request.form['password'])
                        ):
        flash("Login ou senha incorreta")
    return DB.RedirectIndex()
 
@frontend.route("/logout")
def logout():
    DB = ConnectDatabase.getFactory()
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

        DB = ConnectDatabase.getFactory()
        user = DB.getSessionUser()
        DB.CreateTamagotchi(
            name=POST_NOME,
            user_id=user.id,
            imagem=IMAGEM)

        return DB.RedirectIndex()


@frontend.route('/ranking')
def rank():
    DB = ConnectDatabase.getFactory()
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
    DB = ConnectDatabase.getFactory()

    DB.DeleteTamagotchi(request.form['id'])

    return DB.RedirectIndex()

@frontend.route('/tamagotchi/buy', methods=['POST'])
def compraBixo():
    DB = ConnectDatabase.getFactory()

    user = DB.getSessionUser()
    IMAGEM = str(request.form['poke'])

    DB.SavePokemon(name=IMAGEM, user_id=user.id)
