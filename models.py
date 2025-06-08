from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Team(db.Model):
    id    = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(100), nullable=False)

class Player(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    nazwa   = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

class Game(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    nazwa     = db.Column(db.String(100), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    host_id   = db.Column(db.Integer, db.ForeignKey('team.id'))
    guest_id  = db.Column(db.Integer, db.ForeignKey('team.id'))
    wynik     = db.relationship('Wynik', uselist=False, backref='game')

class Wynik(db.Model):
    id                = db.Column(db.Integer, primary_key=True)
    liczba_goli_host  = db.Column(db.Integer, default=0)
    liczba_goli_guest = db.Column(db.Integer, default=0)
    game_id           = db.Column(db.Integer, db.ForeignKey('game.id'))

class Gol(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    strzelec_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    mecz_id     = db.Column(db.Integer, db.ForeignKey('game.id'))
