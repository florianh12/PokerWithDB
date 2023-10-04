from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Double,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from .Cards import Card
from .State import State


db = SQLAlchemy()

class Game(db.Model):
    __tablename__ = 'game'
    
    game_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String,default='',nullable=False)
    table_0 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    table_1 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    table_2 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    table_3 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    table_4 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    current_bet = Column(Double,default=1.0,nullable=False)
    pot = Column(Double,default=0.0,nullable=False)
    turn = Column(Integer,default=-1,nullable=False)
    active = Column(Boolean,default=True,nullable=False)
    
    participants = relationship('Participates', back_populates='participation')

class Player(db.Model):
    __tablename__ = 'player'
    
    username = Column(String(40),primary_key=True)
    password = Column(String(100),nullable=False)
    stash = Column(Double,default=10.0,nullable=False)
    
    participation = relationship('Participates', back_populates='participants')
    
class Participates(db.Model):
    __tablename__ = 'participates'
    
    game_id = Column(Integer,ForeignKey('game.game_id'), primary_key=True)
    player_username = Column(String(40), ForeignKey('player.username'), primary_key=True)
    hand_0 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    hand_1 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    turn_state = Column(Enum(State),default=State.false,nullable=False)
    
    participation = relationship('Game', back_populates='participants')
    participants = relationship('Player', back_populates='participation')