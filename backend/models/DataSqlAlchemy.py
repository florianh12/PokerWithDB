from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .Cards import Card
from sqlalchemy_utils import ChoiceType

db = SQLAlchemy()

class Game(db.Model):
    __tablename__ = 'game'
    
    game_id = Column(Integer, primary_key=True, autoincrement=True)
    table_0 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    table_1 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    table_2 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    table_3 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    table_4 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    
    participants = relationship('Participates', back_populates='participation')

class Player(db.Model):
    __tablename__ = 'player'
    
    username = Column(String(40),primary_key=True)
    password = Column(String(100),nullable=False)
    
    participation = relationship('Participates', back_populates='participants')
    
class Participates(db.Model):
    __tablename__ = 'participates'
    
    game_id = Column(Integer,ForeignKey('game.game_id'), primary_key=True)
    player_username = Column(String(40), ForeignKey('player.username'), primary_key=True)
    hand_0 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    hand_1 = Column(ChoiceType(Card, impl=db.Integer()),nullable=False)
    
    participation = relationship('Game', back_populates='participants')
    participants = relationship('Player', back_populates='participation')