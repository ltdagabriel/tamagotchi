# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

from flask import Flask, flash, redirect, render_template, request, session, abort, redirect

from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///tutorial.db', echo=True)

from flask import Blueprint, render_template
from flask_nav.elements import Navbar, View
from markupsafe import escape

from nav import nav
from datetime import datetime

frontend = Blueprint('frontend', __name__)




# We're adding a navbar as well through flask-navbar. In our example, the
# navbar has an usual amount of Link-Elements, more commonly you will have a
# lot more View instances.
nav.register_element('frontend_top', Navbar(
    View('Tamagotchi', '.home'),
    View('Deslogar', '.logout'),
    View('Criar Tamagotchi', '.novotamagotchi'),
    ))


# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.

def MyTamagotchis(username):
    tamagotchis=[]
    
    s = sessionmaker(bind=engine)()
    user = s.query(User).filter(User.username.in_([session.get('username')])).first()
    query = s.query(Tamagotchi).filter(Tamagotchi.user_id.in_([user.id]) ) 
    return query
    
    tamagotchis.append(Tamagotchi_class)

    return tamagotchis

@frontend.route('/tamagotchiform')
def novotamagotchi():
    return render_template('tamagotchi_form.html')

@frontend.route('/')
def home():
    
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html', tamagotchi=MyTamagotchis("gabriel"), index=0 )
 
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
        flash('wrong password!')
    return home()
 
@frontend.route("/logout")
def logout():
    session['logged_in'] = False
    session['username'] = None
    return home()

@frontend.route('/novotamagotchi', methods=['POST'])
def do_novo_tamagotchi():
 
    POST_NOME = str(request.form['nome'])
    Session = sessionmaker(bind=engine)
    s = Session()
    # print()
    user = s.query(User).filter(User.username.in_([session.get('username')])).first()
    tamago = Tamagotchi(POST_NOME, user.id)

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
    return home()