from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship, sessionmaker
from .Cards import Card


Base = declarative_base()
class Game(Base):
    __tablename__ = 'game'
    
    game_id = Column(Integer, primary_key=True, autoincrement=True)
    table_0 = Column(Enum(Card, native_enum=False),nullable=False)
    table_1 = Column(Enum(Card, native_enum=False),nullable=False)
    table_2 = Column(Enum(Card, native_enum=False),nullable=False)
    table_3 = Column(Enum(Card, native_enum=False),nullable=False)
    table_4 = Column(Enum(Card, native_enum=False),nullable=False)
    
    participants = relationship('Participates', back_populates='participation')

class Player(Base):
    __tablename__ = 'player'
    
    username = Column(String(40),primary_key=True)
    password = Column(String(100),nullable=False)
    
    participation = relationship('Participates', back_populates='participants')
    
class Participates(Base):
    __tablename__ = 'participates'
    
    game_id = Column(Integer,ForeignKey('game.game_id'), primary_key=True)
    player_username = Column(String(40), ForeignKey('player.username'), primary_key=True)
    hand_0 = Column(Enum(Card, native_enum=False),nullable=False)
    hand_1 = Column(Enum(Card, native_enum=False),nullable=False)
    
    participation = relationship('Game', back_populates='participants')
    participants = relationship('Player', back_populates='participation')