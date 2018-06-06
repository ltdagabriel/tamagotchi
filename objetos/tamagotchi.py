# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from session import *
from database import *
from objetos import pokemon, usuario
import _thread
import time
from datetime import timedelta
import humanize
import sys


class LoadTamagotchi():
    def run(self, threadName, delay):
        try:
            lista = ListTamagotchi()
            print("Runing %s %s" % (threadName, delay))
            session = sessionmaker(bind=engine)()
            for x in session.query(Tamagotchi).all():
                if x.id not in [x.tamagotchi.id for x in lista.load_all()]:
                    lista.append(x)
                else:
                    list(lista.load('id', x.id))[0].update()
            session.close()
            time.sleep(1)
            self.run(threadName, delay + 1)
        except ValueError:
            print("Error")


class ObjetoStatus:
    def __init__(self):
        self.status = []

    def setStatus(self, tamagotchi_id, status):
        s = sessionmaker(bind=engine)()
        if not s.query(Status).filter(Status.state.in_([status]), Status.tamagotchi_id.in_([tamagotchi_id])).first():
            status = Status(status, tamagotchi_id)
            s.add(status)
            s.commit()

    def find(self, tamagotchi_id, status):
        s = sessionmaker(bind=engine)()
        status = list(s.query(Status).filter(Status.state.in_([status]), Status.tamagotchi_id.in_([tamagotchi_id])))
        return True if len(status) else False

    def to_json(self, tamagotchi_id):
        s = sessionmaker(bind=engine)()
        status = []
        for x in list(s.query(Status).filter(Status.tamagotchi_id.in_([tamagotchi_id]))):
            statu = {}
            for i in Status.__table__.columns.keys():
                statu.update({i: x.__getattribute__(i)})
            status.append(statu)
        return status

    def removeStatus(self, tamagotchi_id, status):
        s = sessionmaker(bind=engine)()
        status = s.query(Status).filter(Status.state.in_([status]), Status.tamagotchi_id.in_([tamagotchi_id])).first()
        if status:
            s.delete(status)
            s.commit()


class ObjetoTamagotchi:
    def __init__(self, tamagotchi):
        self.poke = pokemon.ListPokemon()
        self.tamagotchi = tamagotchi
        self.happy = []
        self.hunger = []
        self.health = []
        self.status = ObjetoStatus()

    def setstatus(self, status):
        self.status.setStatus(self.tamagotchi.id, status)

    def unsetstatus(self, status):
        self.status.removeStatus(self.tamagotchi.id, status)

    def findstatus(self, status):
        return self.status.find(self.tamagotchi.id, status)

    def removeStatus(self, status):
        self.status.setStatus(self.tamagotchi.id, status)

    def engine(self):
        if self.findstatus('Morto'):
            return

        health = 0.1
        hunger = 0.1
        happy = 0.1

        delta = (datetime.now() - self.tamagotchi.last_update).total_seconds()

        # Atualiza taxa de decaimento dos status
        if self.findstatus('Triste'):
            happy = 0.5

        if self.findstatus('Doente'):
            health = 0.5

        if self.findstatus('Faminto'):
            hunger = 0.5

        # Evolução
        pokelist = pokemon.ListPokemon()
        poke = pokelist.loadDatabasebyName(self.tamagotchi.name_pokemon, self.tamagotchi.user_id)
        poke = poke[0].pokemon

        if poke.evolucao and (datetime.now() - poke.selected).total_seconds() > 60 * 30:
            pokelist.saveDatabase(poke.evolucao, self.tamagotchi.user_id)
            self.tamagotchi.name_pokemon = poke.evolucao

        # atualiza barras
        self.health.append(-1 * delta * health)
        self.happy.append(-1 * delta * happy)
        self.hunger.append(-1 * delta * hunger)

        # atualuza status
        if self.tamagotchi.health <= 0 or self.tamagotchi.hunger <= 0 or self.tamagotchi.happy <= 0:
            self.setstatus('Morto')

        if self.tamagotchi.health < 50:
            self.setstatus('Doente')
        else:
            self.unsetstatus('Doente')

        if self.tamagotchi.hunger < 50:
            self.setstatus('Faminto')
        else:
            self.unsetstatus('Faminto')

        if self.tamagotchi.happy < 50:
            self.setstatus('Triste')
            self.setstatus('Doente')
        else:
            self.unsetstatus('Doente')
            self.unsetstatus('Triste')

    def update(self):
        self.engine()

        s = sessionmaker(bind=engine)()
        tama = s.query(Tamagotchi).filter(Tamagotchi.id.in_([self.tamagotchi.id])).first()

        tama.name_pokemon = self.tamagotchi.name_pokemon

        health = tama.health + sum(self.health)
        tama.health = health if health <= 100 else 100
        self.tamagotchi.health = tama.health
        self.health = []

        hunger = tama.hunger + sum(self.hunger)
        tama.hunger = hunger if hunger <= 100 else 100
        self.tamagotchi.hunger = tama.hunger
        self.hunger = []

        happy = tama.happy + sum(self.happy)
        tama.happy = happy if happy <= 100 else 100
        self.tamagotchi.happy = tama.happy
        self.happy = []

        tama.last_update = datetime.now()
        self.tamagotchi.last_update = tama.last_update

        s.commit()

    def filter(self, by, value):
        return self.tamagotchi.__getattribute__(by) == value

    def calculeage(self):
        time = (self.tamagotchi.last_update - self.tamagotchi.birthday).total_seconds()
        day = time // (24 * 3600)
        time = time % (24 * 3600)
        hour = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        seconds = time

        return "%dd %d:%d:%ds" % (day, hour, minutes, seconds)

    def to_json(self):
        tamagotchi = {}

        poke = self.poke.loadDatabasebyName(self.tamagotchi.name_pokemon, self.tamagotchi.user_id)[0]
        user = usuario.ListUsuario().getbyid(self.tamagotchi.user_id)
        for i in Tamagotchi.__table__.columns.keys():
            tamagotchi.update({i: self.tamagotchi.__getattribute__(i)})

        tamagotchi.update({'age': self.calculeage()})
        tamagotchi.update({'state': self.status.to_json(self.tamagotchi.id)})
        tamagotchi.update({'user_name': user.username})

        return {'tamagotchi': tamagotchi,
                'pokemon': poke.to_json()}


class ListTamagotchi:
    class __ListTamagotchi:
        def __init__(self):
            self.tamagotchis = []

        def append(self, tamagotchi):
            self.tamagotchis.append(ObjetoTamagotchi(tamagotchi))

        def update(self, id, health=None, hunger=None, happy=None):
            for x in list(self.load('id', id)):
                if health:
                    x.health.append(health)
                if hunger:
                    x.hunger.append(hunger)
                if happy:
                    x.happy.append(happy)

        def load_all(self):
            return sorted(self.tamagotchis,
                          key=lambda tama: (tama.tamagotchi.last_update - tama.tamagotchi.birthday).total_seconds(),
                          reverse=True)

        def load(self, by, value):
            return filter(lambda x: x.filter(by, value), self.tamagotchis)

        def saveDatabase(self, name, user_id, imagem):
            s = sessionmaker(bind=engine)()
            tamago = Tamagotchi(
                name=name,
                user_id=user_id,
                imagem=imagem)

            s.add(tamago)
            s.commit()

            return tamago

        def verify_if_exist(self, name):
            s = sessionmaker(bind=engine)()
            poke = s.query(Tamagotchi).filter(Tamagotchi.name.in_([name])).first()
            return True if poke else False

    instance = None

    def __init__(self):
        if not ListTamagotchi.instance:
            ListTamagotchi.instance = ListTamagotchi.__ListTamagotchi()
            try:
                load = LoadTamagotchi()
                _thread.start_new_thread(load.run, ('Load Tamagotchi', 2,))
            except ValueError:
                print("Error: unable to start thread")

    def __getattr__(self, item):
        return getattr(self.instance, item)
