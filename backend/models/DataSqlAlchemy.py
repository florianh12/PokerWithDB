from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Double,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from .Cards import Card
from .State import State


db = SQLAlchemy()

class PokerGame(db.Model):
    __tablename__ = 'PokerGame'
    
    gameID = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String,default='',nullable=False)
    table1 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    table2 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    table3 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    table4 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    table5 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    stake = Column(Double,default=1.0,nullable=False)
    pot = Column(Double,default=0.0,nullable=False)
    round = Column(Integer,default=-1,nullable=False)
    
    participants = relationship('Plays', back_populates='participation')
    won_by = relationship('WonBy', back_populates='winner_of')

class Player(db.Model):
    __tablename__ = 'player'
    
    username = Column(String(40),primary_key=True)
    password = Column(String(100),nullable=False)
    stash = Column(Double,default=10.0,nullable=False)
    
    participation = relationship('Plays', back_populates='participants')
    games_won = relationship('WonBy', back_populates='winning_player')
    
class Plays(db.Model):
    __tablename__ = 'plays'
    
    gameID = Column(Integer,ForeignKey('PokerGame.gameID'), primary_key=True)
    player_username = Column(String(40), ForeignKey('player.username'), primary_key=True)
    hand1 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    hand2 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    status = Column(ChoiceType(State, impl=str()),default=State.unkown,nullable=False)
    paid_this_round = Column(Double,default=0.0,nullable=False)
    
    participation = relationship('PokerGame', back_populates='participants')
    participants = relationship('Player', back_populates='participation')
    

class WonBy(db.Model):
    __tablename__ = 'won_by'
    
    gameID = Column(Integer,ForeignKey('PokerGame.gameID'), primary_key=True)
    username = Column(String(40), ForeignKey('player.username'), primary_key=True)

    winner_of = relationship('PokerGame', back_populates='won_by')
    winning_player = relationship('Player', back_populates='games_won')