from flask import Blueprint, render_template, Markup, url_for, redirect, request, flash, jsonify
from session import Session
from objetos import usuario, tamagotchi, pokemon, hashgame

route = Blueprint('route', __name__)


@route.route('/')
def index():
    sessao = Session()
    user = sessao.get_logged_user()
    if user:
        poke = pokemon.ListPokemon()

        return render_template('tamagotchi.html', titulo="Tamagotchi", pokemons=poke.sale())
    else:
        return redirect(url_for('.login'))


@route.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', titulo="Tamagotchi")
    elif request.method == 'POST':
        sessao = Session()
        if not sessao.login(username=str(request.form['username']),
                            password=str(request.form['password'])):
            flash("Login ou senha incorretos")
    return redirect(url_for('.index'))


@route.route('/logout')
def logout():
    sessao = Session()
    sessao.logout()
    return redirect(url_for('.index'))


@route.route('/cadastrar', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        user = usuario.ListUsuario()
        return render_template('cadastro_usuario.html', titulo="Crie sua conta", personagens=user.get_personagens())
    elif request.method == 'POST':
        sessao = Session()
        USERNAME = str(request.form['username'])
        error = False
        if not USERNAME:
            flash("Campo usuario precisa ser preenchido!")
            error = True

        PASSWORD = str(request.form['password'])
        if not PASSWORD:
            flash("Campo senha necessario!")
            error = True

        IMAGEM = str(request.form['persona'])
        if not IMAGEM:
            flash("é necessario escolher um personagem!")
            error = True

        if not sessao.novo_usuario(USERNAME, PASSWORD, IMAGEM):
            flash("Falha ao criar conta")
            error = True

        if error:
            return redirect(url_for('.cadastro'))

        return redirect(url_for('.login'))


@route.route('/usuarios', methods=['POST'])
def get_user():
    sessao = Session()
    return jsonify({'success': "que isso muleke",
                    'usuarios': list(map(lambda x: x.to_json(), sessao.get_all_logged_user())),
                    'mensagens': [],
                    'status': 'Online'
                    })


@route.route('/tamagotchis/new', methods=['GET', 'POST'])
def novo_tamagotchi():
    sessao = Session()
    user = sessao.get_logged_user()
    if not user:
        return redirect('.index')

    if request.method == 'GET':
        sessao = Session()
        return render_template('cadastro_tamagotchi.html',
                               pokemons=list(map(lambda x: x.pokemon, sessao.get_my_pokemons())),
                               titulo='Criar Tamagotchi'
                               )
    elif request.method == 'POST':
        POST_NOME = request.form['nome']
        IMAGEM = request.form['poke']
        error = False

        sessao = Session()
        if sessao.verify_if_exist(POST_NOME):
            flash("Ja existe um tamagotchi com este nome")
            error = True

        if not error:
            sessao = Session()
            user = sessao.get_logged_user()

            tamagotchi.ListTamagotchi().saveDatabase(
                name=POST_NOME,
                user_id=user.id,
                imagem=IMAGEM)

            return redirect(url_for('.index'))
        else:
            return redirect(url_for('.novo_tamagotchi'))


@route.route('/tamagotchis/user', methods=['POST'])
def get_tamagotchis():
    if request.method == 'POST':
        sessao = Session()
        user = sessao.get_logged_user()
        if not user:
            return redirect('.index')

        tamagotchis = sessao.load_tamagotchi('user_id', user.id)

        return jsonify(list(map(lambda x: x.to_json(), tamagotchis)))
    else:
        return redirect('.index')


@route.route('/tamagotchis', methods=['POST'])
def get_all_tamagotchis():
    if request.method == 'POST':
        sessao = Session()
        user = sessao.get_logged_user()

        tamagotchis = sessao.load_tamagotchi()

        return jsonify(list(map(lambda x: x.to_json(), tamagotchis)))
    else:
        return redirect('.index')


@route.route('/tamagotchi', methods=['POST'])
def get_tamagotchi():
    if request.method == 'POST':
        sessao = Session()
        user = sessao.get_logged_user()
        if not user:
            return redirect('.index')
        id = int(request.form['id'])
        if id:
            tamagotchi = sessao.load_tamagotchi('id', id)
        else:
            tamagotchi = sessao.load_tamagotchi('user_id', user.id)
        return jsonify(list(map(lambda x: x.to_json(), tamagotchi)))
    else:
        return redirect('.index')


@route.route('/tamagotchi/update', methods=['POST'])
def actions():
    if request.method == 'POST':
        list = tamagotchi.ListTamagotchi()

        id = int(request.form['id'])
        value = int(request.form['value'])
        action = str(request.form['action'])

        if action == 'health':
            list.update(id=id, health=value)

        if action == 'hunger':
            list.update(id=id, hunger=value)

        if action == 'happy':
            list.update(id=id, happy=value)
        return jsonify({'action': action,
                        'value': value,
                        'id': id})
    return jsonify({'error': 'metodo invalido'})


@route.route('/tamagotchi/buy', methods=['POST'])
def buy():
    PRICE = float(request.form['price'])
    IMAGEM = str(request.form['poke'])

    poke = pokemon.ListPokemon()

    user = usuario.ListUsuario().get_logged_user()

    if user.money > PRICE:
        poke.buy(PRICE, IMAGEM, user.id)
    else:
        flash("Voce so tem $ " + str(user.money) + " falta $ " + str(PRICE - user.money) + ".")
    return redirect(url_for('.index'))


@route.route('/user/get', methods=['POST'])
def getUser():
    user = usuario.ListUsuario().get_logged_user()
    return jsonify({'user': {'username': user.username,
                             'img': user.imagem,
                             'money': user.money}})


@route.route('/mensagem', methods=['POST', 'GET'])
def chat():
    sessao = Session()
    if request.method == 'POST':
        msg = str(request.form['msg'])
        user = sessao.get_logged_user()
        sessao.sendmensagem(msg, user)
        return redirect(url_for('.index'))
    if request.method == 'GET':
        return jsonify(list(map(lambda x: x.to_json(), sessao.getmensagem())))

@route.route('/games/jogo_da_velha', methods=['POST'])
def load_hash():
    user = usuario.ListUsuario().get_logged_user()
    if user:
        if str(request.form['game_name']) == 'Jogo_da_Velha':
            return hashgame.hashgame().game(comand=str(request.form['comand']),
                                            game=request.form['game'],
                                            param=str(request.form['param']),
                                            player=user.username)
    return jsonify({'error': 'Algo de errado aconteceu'})


@route.route('/info/<idioma>')
@route.route('/info')
def comoJogar(idioma='pt-br'):
    return render_template('comoJogar.html', titulo="Como jogar", idioma=idioma)


@route.route('/ranking')
def ranking():
    return render_template('ranking.html', titulo="Ranking")




@route.route('/reward', methods=['POST'])
def Reward():
    player1 = str(request.form['player1'])
    player2 = str(request.form['player2'])
    usuario.ListUsuario().UserReward(int(request.form['reward']), player1)
    if player2:
        usuario.ListUsuario().UserReward(int(request.form['reward']), player2)

    return jsonify({'success': 'usuario recebeu sua recompensa!'})
