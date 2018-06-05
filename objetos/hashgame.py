# -*- coding: utf-8 -*-
from flask import jsonify
from datetime import datetime
from random import randint


class Objetohashgame():

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

        self.player1_msg = []
        self.player2_msg = []

    def LoadMovements(self, player):
        movimentos_possiveis = []

        random_movements = ['00', '01', '02', '10', '11', '12', '20', '21', '22']

    def verifica_movimento(self, movement):
        linha = movement[0]
        coluna = movement[1]

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
            if nivel == 1:
                return peca
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
                'player1_msg': self.player1_msg,
                'player2_msg': self.player2_msg,
                'next': self.next_piece,
                'player1_piece': self.player1_piece,
                'player2_piece': self.player2_piece,
                'board': self.board,
                'key': self.key,
                'idle': int((datetime.now() - self.last_action).total_seconds())
                }


class hashgame():
    class __hashgame():
        def __init__(self):
            self.games = []

        def game(self, comand=None, game=None, param=None, player=None):

            if not comand:
                return None

            if not self.games:
                self.games = []

            if comand == 'New':

                pieces = ['X', 'O']
                rand = randint(0, 1)
                key = len(self.games)
                self.games.append(Objetohashgame(player1=player,
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
        if not hashgame.instance:
            hashgame.instance = hashgame.__hashgame()

    def __getattr__(self, item):
        return getattr(self.instance, item)
