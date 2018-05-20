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


# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.
def UpdateTamagotchi(tamagotchi):
    if tamagotchi:
        s = sessionmaker(bind=engine)()
        if ( tamagotchi.state == 'Morto'):
            return "It's Dead"


        hungerRate = 0.01
        healthRate = 0.01
        happyRate = 0.01
        deltaTime = (datetime.now() - tamagotchi.last_update).total_seconds()
        if( 30*60 < int(deltaTime) < 60*60):
            tamagotchi.name_pokemon= tamagotchi.name_pokemon[0:-1]+'2'
            Pokemon1 = Pokemon(tamagotchi.name_pokemon, user.id, True)
            s.add(Pokemon1)
        
        elif( 60*60 < int(deltaTime)):
            tamagotchi.name_pokemon= tamagotchi.name_pokemon[0:-1]+'3'
            Pokemon2 = Pokemon(tamagotchi.name_pokemon, user.id, True)
            s.add(Pokemon2)

        tamagotchi.last_update = datetime.now()
        if (tamagotchi.happy <= 0 or tamagotchi.health <= 0 or tamagotchi.hunger <= 0):
            tamagotchi.state = 'Morto'

        # atualiza estados
        elif (tamagotchi.happy < 60):
            tamagotchi.state = 'Triste'

        elif (tamagotchi.health < 60):
            tamagotchi.state = 'Doente'

        elif (tamagotchi.hunger < 60):
            tamagotchi.state = 'Faminto'

        

        if (tamagotchi.state == 'Doente'):
            healthRate = 0.06

        if (tamagotchi.state == 'Faminto'):
            hungerRate = 0.05

        if (tamagotchi.state == 'Triste'):
            happyRate = 0.07

        tamagotchi.hunger = tamagotchi.hunger - hungerRate * deltaTime if tamagotchi.hunger - hungerRate * deltaTime >= 0 else 0
        tamagotchi.happy = tamagotchi.happy - happyRate * deltaTime if tamagotchi.happy - happyRate * deltaTime >= 0 else 0
        tamagotchi.health = tamagotchi.health - healthRate * deltaTime if tamagotchi.health - healthRate * deltaTime >= 0 else 0

        s.commit()
        return tamagotchi
    else:
        return redirect(url_for('.index'))

def MyTamagotchis(id=None):
    s = sessionmaker(bind=engine)()
    user = s.query(User).filter(User.username.in_([session.get('username')])).first()
    if id:
        query = s.query(Tamagotchi).filter(Tamagotchi.id.in_([id]), Tamagotchi.user_id.in_([user.id])).first()
    else:
        query = s.query(Tamagotchi).filter(Tamagotchi.user_id.in_([user.id]))
    return query

def AllTamagotchis():
    s = sessionmaker(bind=engine)()
    todos = s.query(Tamagotchi).all()
    for tamagotchi in todos:
        UpdateTamagotchi(tamagotchi)

    return sorted(todos, key= lambda tama: (tama.last_update - tama.birthday).total_seconds(), reverse= True)



def getSessionUser():
    s = sessionmaker(bind=engine)()
    username= session.get('username')
    if username:
        return s.query(User).filter(User.username.in_([username])).first()
    else:
        return None

def getPokemon(name,user_id=None):
    s = sessionmaker(bind=engine)()
    if user_id:
        return s.query(Pokemon).filter(Pokemon.name.in_([name]), Pokemon.user_id.in_([user_id]) ).first()
    else:
        return s.query(Pokemon).filter(Pokemon.name.in_([name])).first()

def getPokemonList(user_id=None):
    s = sessionmaker(bind=engine)()
    if user_id:
        return s.query(Pokemon).filter( Pokemon.user_id.in_([user_id]) )
    else:
        return []

def getUserTamagotchi(user_id=None):
    s = sessionmaker(bind=engine)()
    if user_id:
        tamagotchis = []
        for tama in s.query(Tamagotchi).filter(Tamagotchi.user_id.in_([user_id])):
            tamagotchis.append( UpdateTamagotchi(tama))
        return tamagotchis
    else: 
        return []
    
def getTamagotchi(id=None, dead=False):
    s = sessionmaker(bind=engine)()
    if id:
        value = []
        if dead:
            tama= s.query(Tamagotchi).filter( Tamagotchi.id.in_([id]), Tamagotchi.state.notin_(['Dead']) )
        
        else:
            tama = s.query(Tamagotchi).filter( Tamagotchi.id.in_([id]) )
        
        for i in tama:
            value.append(UpdateTamagotchi(i))
        
        if len(value):
            return value[0]
        else:
            return None
    else:
        return None

@frontend.route('/load', methods=['POST'])
def load_tamagotchi():
    # Pega id do tamagotchi pego por requisicao ajax
    id = int(request.form['id'])

    # Carregar Usuario logado
    user = getSessionUser()
    if user:
        # Carregar meus tamagotchis
        tamagotchis = getUserTamagotchi(user.id)

        # Pega Tamagotchi pelo id
        tamagotchi = getTamagotchi(id)
        if tamagotchi:
            # Carregar Pokemon
            pokemon =getPokemon(tamagotchi.name_pokemon,user.id)
            
            return jsonify( 
                {
                    'name': tamagotchi.name,
                    'happy': tamagotchi.happy,
                    'hunger': tamagotchi.hunger,
                    'health': tamagotchi.health,
                    'pokemon': {'name':pokemon.name,'cenario':pokemon.cenario},
                    'age': (tamagotchi.last_update - tamagotchi.birthday).total_seconds(),
                    'list': map( lambda tama: ({'id': tama.id,'name': tama.name, 'state': tama.state, 'pokemon': tama.name_pokemon}) ,tamagotchis)
                })
        else:
            return jsonify({'error':" Tamagotchi nao existe"})
    else:
        return jsonify({'error':" Usuario nao esta logado"})


@frontend.route('/tamagotchiform')
def novotamagotchi():
    user = getSessionUser()
    if user:
        pokemons = getPokemonList(user.id)
        return render_template('tamagotchi_form.html', pokemons= pokemons)
    else:
        return redirect(url_for('.index'))


@frontend.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        user = getSessionUser()
        if user:
            tama = getUserTamagotchi(user.id)
            
            if len(tama):
                tama= tama[0]
                return redirect(url_for('.home', id=tama.id))
            else:
                return redirect(url_for('.home'))


@frontend.route('/tamagotchi/<id>/health')
@frontend.route('/tamagotchi/<id>/health/<value>')
def health(id=None, value=20):
    s = sessionmaker(bind=engine)()
    tama = s.query(Tamagotchi).filter(Tamagotchi.id.in_([id])).first()
    tama.health = tama.health + float(value) if tama.health + float(value) <= 100 else 100
    s.commit()
    return redirect(url_for('.home', id=id))


@frontend.route('/tamagotchi/<id>/hunger')
@frontend.route('/tamagotchi/<id>/hunger/<value>')
def hunger(id=None, value=20):
    s = sessionmaker(bind=engine)()
    tama = s.query(Tamagotchi).filter(Tamagotchi.id.in_([id])).first()
    tama.hunger = tama.hunger + float(value) if tama.hunger + float(value) <= 100 else 100
    s.commit()
    return redirect(url_for('.home', id=id))


@frontend.route('/tamagotchi/<id>/happy')
@frontend.route('/tamagotchi/<id>/happy/<value>')
def happy(id=None, value=20):
    s = sessionmaker(bind=engine)()
    tama = s.query(Tamagotchi).filter(Tamagotchi.id.in_([id])).first()
    tama.happy = tama.happy + float(value) if tama.happy + float(value) <= 100 else 100
    s.commit()
    return redirect(url_for('.home', id=id))


@frontend.route('/tamagotchi')
@frontend.route('/tamagotchi/<id>')
def home(id=None):
    if id:
        tama= getTamagotchi(id)
        return render_template('index.html', tamagotchis=MyTamagotchis(), tamagotchi=tama)
    else:
        return render_template('welcome.html')


@frontend.route('/cadastrar')
def cadastro():
    return render_template('user_form.html')

@frontend.route('/login', methods=['POST'])
def do_admin_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
        session['username'] = POST_USERNAME
    else:
        flash('"wrong" password!')
    return redirect(url_for('.index'))
 
@frontend.route("/logout")
def logout():
    session['logged_in'] = False
    session['username'] = None
    return redirect(url_for('.index'))

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
        Session = sessionmaker(bind=engine)
        s = Session()
        user = s.query(User).filter(User.username.in_([session.get('username')])).first()
        tamago = Tamagotchi(POST_NOME, user.id, IMAGEM)

        s.add(tamago)

        s.commit()

        return redirect(url_for('.index'))



@frontend.route('/cadastrar/novo', methods=['POST'])
def cadastrar():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    user = User(POST_USERNAME,POST_PASSWORD)

    s.add(user)
    s.commit()
    Pokemon1 = Pokemon("bul1", user.id, True)
    s.add(Pokemon1)
    Pokemon2 = Pokemon("char1", user.id,False)
    s.add(Pokemon2)    
    Pokemon3 = Pokemon("sqr1", user.id,False)
    s.add(Pokemon3)

    s.commit()


    return redirect(url_for('.index'))

@frontend.route('/ranking')
def rank():
    return render_template('rank.html', tamagotchis=AllTamagotchis(), pegaCriadorDoTamagotchi=pegaCriadorDoTamagotchi)

def pegaCriadorDoTamagotchi(id):
    s = sessionmaker(bind=engine)()
    return s.query(User).filter(User.id.in_([id]))

def verificaNome(nome):
    s = sessionmaker(bind=engine)()

    teste = s.query(Tamagotchi).filter(Tamagotchi.name.in_([nome])).first()

    if teste:
        return True
    else:
        return False

@frontend.route('/tamagotchi/del', methods=['POST'])
def deletaBixo():
    s = sessionmaker(bind=engine)()
    id = request.form['id']
    tama = s.query(Tamagotchi).filter(Tamagotchi.id.in_([int(id)])).first()
    s.delete(tama)
    s.commit()
    return redirect(url_for('.index'))

@frontend.route('/tamagotchi/<id>', methods=['POST'])
def compraBixo():
    s = sessionmaker(bind=engine)()
    IMAGEM = str(request.form['poke'])
    # Pokemon1 = Pokemon(IMAGEM, user.id)
    # s.add(Pokemon1)
    user = s.query(User).filter(User.username.in_([session.get('username')])).first()
    tamago = Tamagotchi(POST_NOME, user.id, IMAGEM)

    s.add(tamago)

    s.commit()