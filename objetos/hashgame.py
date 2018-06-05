# -*- coding: utf-8 -*-
from flask import jsonify
from datetime import datetime
from random import randint
from objetos import usuario


class Objetohashgame():

    def __init__(self, player1=None, player2=None, key=None, player1_piece=None, player2_piece=None):
        self.player1 = player1
        self.player2 = player2
        self.key = key
        self.winner = None
        self.player_winner = None
        self.next_piece = 'X'
        self.player1_piece = player1_piece
        self.player2_piece = player2_piece
        self.board = [['B', 'B', 'B'],
                      ['B', 'B', 'B'],
                      ['B', 'B', 'B']]
        self.state = 'Game Started'
        self.last_action = datetime.now()

        self.player1_msg = ""
        self.player2_msg = ""

        self.valid = True if len(self.LoadMovements()) else False

    def machineMove(self):
        moves = self.LoadMovements()
        move = moves[randint(0, len(moves)-1)]

        self.Movement(player=self.player2, casa=move)

    def reward(self):

        consolacao = 10
        recompensa = 20

        if self.player1_piece == self.winner:
            self.player_winner = self.player1
            if self.player1 == 'machine':
                usuario.ListUsuario().UserReward(consolacao, self.player2)
                self.player2_msg = "Você perdeu, premio de consolação:  $" + str(consolacao) + ",00"
            else:
                self.player2_msg = "Você perdeu, premio de consolação:  $" + str(consolacao) + ",00"
                usuario.ListUsuario().UserReward(consolacao, self.player2)
                usuario.ListUsuario().UserReward(recompensa, self.player1)
                self.player1_msg = "Você venceu, recompensa adquirida:  $" + str(recompensa) + ",00"
        elif self.player2_piece == self.winner:
            self.player_winner = self.player2
            if self.player2 == 'machine':
                usuario.ListUsuario().UserReward(consolacao, self.player1)
                self.player1_msg = "Você perdeu, premio de consolação:  $" + str(consolacao) + ",00"
            else:
                self.player1_msg = "Você perdeu, premio de consolação:  $" + str(consolacao) + ",00"
                usuario.ListUsuario().UserReward(consolacao, self.player1)
                usuario.ListUsuario().UserReward(recompensa, self.player2)
                self.player2_msg = "Você venceu, recompensa adquirida:  $" + str(recompensa) + ",00"
        else:
            if self.player1 == 'machine':
                usuario.ListUsuario().UserReward(consolacao, self.player2)
                self.player2_msg = "Empate, premio de consolação:  $" + str(consolacao) + ",00"
            elif self.player2 == 'machine':
                usuario.ListUsuario().UserReward(consolacao, self.player1)
                self.player1_msg = "Empate, premio de consolação:  $" + str(consolacao) + ",00"
            else:
                usuario.ListUsuario().UserReward(consolacao, self.player1)
                usuario.ListUsuario().UserReward(consolacao, self.player2)
                self.player1_msg = "Empate, premio de consolação:  $" + str(consolacao) + ",00"
                self.player2_msg = "Empate, premio de consolação:  $" + str(consolacao) + ",00"

    def update(self):
        self.valid = True if len(self.LoadMovements()) else False
        if not self.valid:
            self.winner = 'B'
            self.reward()
        d1 = []
        d2 = []

        for i in range(0, 3):
            v1 = []
            v2 = []
            for j in range(0, 3):
                v1.append(self.board[i][j])
                v2.append(self.board[j][i])

                if i == j:
                    d1.append(self.board[i][j])
                if i + j == 2:
                    d2.append(self.board[i][j])

            if v1.count('X') == 3:
                self.winner = 'X'
                self.reward()
                return
            elif v1.count('O') == 3:
                self.winner = 'O'
                self.reward()
                return

            if v2.count('X') == 3:
                self.winner = 'X'
                self.reward()
                return
            elif v2.count('O') == 3:
                self.winner = 'O'
                self.reward()
                return

        if d1.count('X') == 3:
            self.winner = 'X'
            self.reward()
            return
        elif d1.count('O') == 3:
            self.winner = 'O'
            self.reward()
            return

        if d2.count('X') == 3:
            self.winner = 'X'
            self.reward()
            return
        elif d2.count('O') == 3:
            self.winner = 'O'
            self.reward()
            return

    def LoadMovements(self):
        moves = ['00', '01', '02', '10', '11', '12', '20', '21', '22']
        movimentos_possiveis = list(filter(self.valid_moves, moves))
        bestmove = []
        for i in movimentos_possiveis:
            x = self.verifica_movimento(i)
            if x:
                bestmove.append(x)
        if len(bestmove):
            return bestmove
        return movimentos_possiveis

    def verifica_movimento(self, movement):
        linha = int(movement[0])
        coluna = int(movement[1])

        modded = []

        d1 = []
        d2 = []

        for i in range(0, 3):
            v1 = []
            v2 = []
            for j in range(0, 3):
                if linha == i:
                    v1.append(self.board[i][j])
                if coluna == i:
                    v2.append(self.board[j][i])
                if i == j:
                    d1.append(self.board[i][j])
                if i + j == 2:
                    d2.append(self.board[i][j])

            modded.append(v1)
            modded.append(v2)

        if linha == coluna:
            modded.append(d1)
        if linha + coluna == 2:
            modded.append(d2)

        opcoes = []

        for x in modded:
            peca, nivel = self.level_line(x)
            opcoes.append({'peca': peca, 'nivel': nivel})
            if nivel == 2:
                return movement

        return None

    def level_line(self, line):
        X = line.count('X')
        B = line.count('B')
        O = line.count('O')
        if X == 3:
            return 'X', 1
        elif O == 3:
            return 'O', 1
        elif X == 2 and B == 1:
            return 'X', 2
        elif O == 2 and B == 1:
            return 'O', 2
        else:
            return 'B', 3

    def valid_moves(self, movement):
        linha = int(movement[0])
        coluna = int(movement[1])
        if self.board[linha][coluna] == 'B':
            return True
        return False

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

        self.update()

    def isMachine(self):
        if self.player2 == 'machine' and self.player2_piece == self.next_piece:
            return True
        elif self.player1 == 'machine' and self.player1_piece == self.next_piece:
            return True
        return False

    def get(self):
        self.update()
        return {'player1': self.player1,
                'player2': self.player2,
                'player1_msg': self.player1_msg,
                'player2_msg': self.player2_msg,
                'next': self.next_piece,
                'winner': self.winner,
                'player_winner': self.player_winner,
                'player1_piece': self.player1_piece,
                'player2_piece': self.player2_piece,
                'board': self.board,
                'valid': self.valid,
                'key': self.key,
                'idle': int((datetime.now() - self.last_action).total_seconds())
                }


class hashgame():
    class __hashgame():
        def __init__(self):
            self.games = []

        def load(self):
            return self.games

        def game(self, comand=None, game=None, param=None, player=None):

            if not comand:
                return None

            if not self.games:
                self.games = []

            if comand == 'New':
                pieces = ['X', 'O']
                rand = randint(0, 1)
                key = len(self.games)
                player2 = None
                if param == 'pvm':
                    player2 = 'machine'
                self.games.append(Objetohashgame(player1=player,
                                                 player2=player2,
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
                if self.games[key].isMachine():
                    self.games[key].machineMove()

                return jsonify({'key': key,
                                'game': self.games[key].get()})

            if comand == 'Move':
                self.games[int(game)].Movement(player=player,
                                               casa=param)
                self.games[int(game)].update()
                key = int(game)
                return jsonify({'key': key,
                                'game': self.games[key].get()})

            if comand == 'All':
                return jsonify({'games': list(map(lambda x: x.get(), self.games))})

    instance = None

    def __init__(self):
        if not hashgame.instance:
            hashgame.instance = hashgame.__hashgame()

    def __getattr__(self, item):
        return getattr(self.instance, item)
