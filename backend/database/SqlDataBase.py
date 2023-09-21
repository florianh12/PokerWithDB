from flask_sqlalchemy import SQLAlchemy
from typing import List

from .DataBase import DataBase
from models import Card, Player, Game, Participates
import random
import bcrypt


class SqlDataBase(DataBase):

    def __init__(self, db: SQLAlchemy) -> None:
        self.mysqldb = db
        self.mysqlDateFormat = "%Y-%m-%d"
    
            
    
    def create_player(self, username:str, password:str) -> None:
        
        self.mysqldb.session.add(Player(username=username,password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())))
        
        self.mysqldb.session.commit()
        
    def create_game(self, players: List[str]) -> None:
        cards = list(Card)
        random.shuffle(cards)
        to_insert_game = Game(table_0=cards.pop().value,table_1=cards.pop().value,table_2=cards.pop().value,table_3=cards.pop().value,table_4=cards.pop().value)
        
        self.mysqldb.session.add(to_insert_game)
        for player in players:
            self.mysqldb.session.add(Participates(game_id=to_insert_game.game_id,player_username=player,hand_0=cards.pop().value,hand_1=cards.pop().value))
        
        self.mysqldb.session.commit()

    def get_games(self, username:str) -> List[Game]:
        return self.mysqldb.session.query(Game).join(Participates, Game.game_id == Participates.game_id).filter_by(player_username=username).all()

    def get_players(self,game:Game) -> List[Player]:
        return self.mysqldb.session.query(Player).join(Participates, Participates.player_username == Player.username).filter_by(game_id=game.game_id).all()

    def login(self, username:str, pwd:str) -> bool:
        hash = Player.query.filter_by(username=username).with_entities(Player.password).first()[0]

        if hash is None: 
            return False
        
        return bcrypt.checkpw(password=pwd.encode('utf-8'),hashed_password=hash[0].encode('utf-8'))
    
    def clear(self) -> None:
        Player.query.delete()
        Game.query.delete()
        Participates.query.delete()
        