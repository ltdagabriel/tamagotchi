# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

from flask import flash, url_for, request, session, redirect

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
def UpdateTamagotchi(s,tamagotchi):

    hungerRate = 5
    healthRate = 5
    happyRate = 5
    deltaTime = (datetime.now() - tamagotchi.last_update).total_seconds()

    tamagotchi.last_update = datetime.now()

    # atualiza estados
    if (tamagotchi.happy < 25):
        tamagotchi.state = 'Triste'

    elif (tamagotchi.health < 25):
        tamagotchi.state = 'Doente'

    elif (tamagotchi.hunger < 60):
        tamagotchi.state = 'Faminto'

    elif (tamagotchi.happy <= 0 or tamagotchi.health <= 0 or tamagotchi.hunger <= 0):
        tamagotchi.state = 'Morto'

    if (tamagotchi.state == 'Saudavel'):
        hunger_lost = hungerRate * 0.01 * deltaTime
        health_lost = healthRate * 0.01 * deltaTime
        happy_lost = happyRate * 0.01 * deltaTime
    elif (tamagotchi.state == 'Doente'):
        hunger_lost = hungerRate * 0.03 * deltaTime
        health_lost = healthRate * 0.03 * deltaTime
        happy_lost = happyRate * 0.03 * deltaTime
    elif (tamagotchi.state == 'Faminto'):
        hunger_lost = hungerRate * 0.02 * deltaTime
        health_lost = healthRate * 0.02 * deltaTime
        happy_lost = happyRate * 0.02 * deltaTime
    elif (tamagotchi.state == 'Triste'):
        hunger_lost = hungerRate * 0.05 * deltaTime
        health_lost = healthRate * 0.05 * deltaTime
        happy_lost = happyRate * 0.05 * deltaTime



    tamagotchi.hunger = tamagotchi.hunger - hunger_lost
    tamagotchi.happy = tamagotchi.happy - happy_lost
    tamagotchi.health = tamagotchi.health - health_lost


    s.commit()


def MyTamagotchis(id=None):
    s = sessionmaker(bind=engine)()
    user = s.query(User).filter(User.username.in_([session.get('username')])).first()
    if id:
        query = s.query(Tamagotchi).filter(Tamagotchi.id.in_([id])).first()
    else:
        query = s.query(Tamagotchi).filter(Tamagotchi.user_id.in_([user.id]))

        for tamagotchi in query:
            UpdateTamagotchi(s, tamagotchi)
    return query

def AllTamagotchis():
    s = sessionmaker(bind=engine)()
    todos = s.query(Tamagotchi).all()

    return todos

@frontend.route('/tamagotchiform')
def novotamagotchi():
    return render_template('tamagotchi_form.html')

@frontend.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        tama = MyTamagotchis().first()
        if tama:
            return redirect(url_for('.home', id=tama.id))
        else:
            return redirect(url_for('.home'))

@frontend.route('/tamagotchi')
@frontend.route('/tamagotchi/<id>')
def home(id=None):
    if id:
        tama= MyTamagotchis(id)
        return render_template('index.html', tamagotchis=MyTamagotchis(), tamagotchi=tama, now=(datetime.now()- tama.birthday) )
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
    Session = sessionmaker(bind=engine)
    s = Session()
    # print()
    user = s.query(User).filter(User.username.in_([session.get('username')])).first()
    tamago = Tamagotchi(POST_NOME, user.id, IMAGEM)

    s.add(tamago)

    s.commit()

    return  redirect('/')
 


@frontend.route('/cadastrar/novo', methods=['POST'])
def cadastrar():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    user = User(POST_USERNAME,POST_PASSWORD)

    s.add(user)

    s.commit()
    return redirect(url_for('.index'))

@frontend.route('/ranking')
def rank():
    return render_template('rank.html', tamagotchis=AllTamagotchis())