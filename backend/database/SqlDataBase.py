from flask_sqlalchemy import SQLAlchemy
from typing import List

from .DataBase import DataBase
from models import Card, Player, Game, Participates,db
import random
import bcrypt


class SqlDataBase(DataBase):

    def __init__(self, app) -> None:
        self.mysqldb = db
        self.mysqldb.init_app(app)
        self.mysqlDateFormat = "%Y-%m-%d"
    
            
    
    def create_player(self, username:str, password:str) -> None:
        
        self.mysqldb.session.add(Player(username=username,password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())))
        
        self.mysqldb.session.commit()
        
    def create_game(self, players: List[str]) -> None:
        cards = list(Card)
        random.shuffle(cards)
        to_insert_game = Game(table_0=cards.pop(),table_1=cards.pop(),table_2=cards.pop(),table_3=cards.pop(),table_4=cards.pop())
        
        self.mysqldb.session.add(to_insert_game)
        self.mysqldb.session.commit()
        for player in players:
            self.mysqldb.session.add(Participates(game_id=to_insert_game.game_id,player_username=player,hand_0=cards.pop(),hand_1=cards.pop()))
        
        self.mysqldb.session.commit()

    def get_games(self, username:str) -> List[Game]:
        return self.mysqldb.session.query(Game).join(Participates, Game.game_id == Participates.game_id).filter_by(player_username=username).all()

    def get_players(self,game:Game) -> List[Participates]:
        return Participates.query.filter_by(game_id=game.game_id).all()

    def login(self, username:str, pwd:str) -> bool:
        hash :str = Player.query.filter_by(username=username).with_entities(Player.password).first()

        if hash is None: 
            return False
        
        hash = hash[0]
        
        return bcrypt.checkpw(password=pwd.encode('utf-8'),hashed_password=hash.encode('utf-8'))
    
    def clear(self) -> None:
        Player.query.delete()
        Game.query.delete()
        Participates.query.delete()
        